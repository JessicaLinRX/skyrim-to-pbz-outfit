"""Validate an explicit runtime manifest and create a new PBZ AIO ZIP.

Python 3.10+, standard library only. No Cook, installation, or manager mutation.
Supports complete unpartitioned pak/utoc/ucas triples and an optional private Lua mod.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,re,zipfile

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def prepare(manifest,base):
    if not isinstance(manifest.get('name'),str) or not manifest['name'].strip():raise ValueError('AIO name is required')
    if not str(manifest.get('version','')).strip():raise ValueError('AIO version is required')
    mod=manifest.get('lua_mod_id')
    if mod is not None and (not isinstance(mod,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',mod)):
        raise ValueError('Invalid lua_mod_id')
    if not isinstance(manifest['files'],list) or not manifest['files']:raise ValueError('Explicit files list is required')
    plans=[];seen=set();containers={}
    lua_prefix=f'platform/steam/ue4ss/Mods/{mod}/' if mod is not None else None
    for f in manifest['files']:
        dest=f['destination']
        if not isinstance(dest,str) or '\\' in dest or ':' in dest:raise ValueError('Use canonical game-relative POSIX destinations')
        path=PurePosixPath(dest)
        if path.is_absolute() or '..' in path.parts or path.as_posix()!=dest:raise ValueError('Invalid destination path')
        if dest.casefold() in seen:raise ValueError('Duplicate destination on Windows')
        seen.add(dest.casefold())
        pak_prefix='ProjectPBZ/Content/Paks/~mods/'
        if dest.startswith(pak_prefix):
            name=dest[len(pak_prefix):];p=PurePosixPath(name)
            if '/' in name or p.suffix not in ('.pak','.utoc','.ucas'):raise ValueError('Expected flat PAK/UTOC/UCAS release paths')
            if not re.fullmatch(r'[A-Za-z0-9_~-]+',p.stem) or p.stem.lower() in ('global','projectpbz-windows'):
                raise ValueError('Refusing global/game container or invalid name')
            containers.setdefault(p.stem.casefold(),set()).add(p.suffix)
        elif lua_prefix is not None and dest.startswith(lua_prefix):
            relative=dest[len(lua_prefix):]
            if relative!='enabled.txt' and not (relative.startswith('Scripts/') and relative.endswith('.lua')):
                raise ValueError('Only enabled.txt and author-owned Scripts/*.lua belong in the Lua payload')
        else:raise ValueError('Destination outside this outfit runtime layout')
        source=Path(f['source']);source=(base/source).resolve() if not source.is_absolute() else source.resolve()
        expected=f['sha256']
        if not re.fullmatch(r'[A-Fa-f0-9]{64}',expected):raise ValueError('Each payload needs an actual SHA256')
        if not source.is_file() or sha(source)!=expected.lower():raise ValueError(f'Payload missing or hash mismatch: {source}')
        plans.append((source,dest,expected.lower(),source.stat().st_size))
    if not containers or any(ext!={'.pak','.utoc','.ucas'} for ext in containers.values()):raise ValueError('Every container requires a complete pak/utoc/ucas triple')
    if lua_prefix is not None:
        for required in ('enabled.txt','Scripts/main.lua'):
            if (lua_prefix+required).casefold() not in seen:raise ValueError('Missing UE4SS '+required)
    return plans

def package(manifest_path,output):
    manifest_path=Path(manifest_path).resolve();output=Path(output).resolve()
    manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    plans=prepare(manifest,manifest_path.parent)
    public={'name':manifest['name'],'version':str(manifest['version'])}
    if manifest.get('lua_mod_id') is not None:
        public['lua_mod_id']=manifest['lua_mod_id']
    public.update(dependencies=manifest.get('dependencies',[]),
                  files=[{'path':d,'sha256':h,'bytes':n} for _,d,h,n in plans])
    output.parent.mkdir(parents=True,exist_ok=True)
    # Exclusive creation also protects against a race with an existing release.
    created=False
    try:
        with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            created=True
            for source,dest,_,_ in plans:z.write(source,dest)
            z.writestr('manifest.json',json.dumps(public,ensure_ascii=False,indent=2))
        with zipfile.ZipFile(output) as z:
            if z.testzip() is not None:raise ValueError('ZIP CRC check failed')
            for _,dest,expected,_ in plans:
                h=hashlib.sha256()
                with z.open(dest) as f:
                    for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
                if h.hexdigest()!=expected:raise ValueError('ZIP contents differ from approved payload')
    except BaseException:
        if created:output.unlink()
        raise
    return {'zip':str(output),'bytes':output.stat().st_size,'sha256':sha(output),'payloadFiles':len(plans),'crcVerified':True,'installed':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(package(a.manifest,a.output),ensure_ascii=False))

if __name__=='__main__':main()

def _parse() :
    import sys
    global _cmd_dict
    _cmd_dict = {}

    cmds = sys.argv[1:]
    cmdi = 0
    
    for cmd in cmds :
        cmdi += 1
        parts = cmd.split("=")
        if len(parts) == 1 : _cmd_dict[cmdi] = parts[0]
        else :
            tag,value = parts
            _cmd_dict[tag] = value  # store all vals as strings

def Int(tag,default=0) :
    return int(_cmd_dict.get(tag,default))

def Float(tag,default=0.0) :
    return float(_cmd_dict.get(tag,default))

def Str(tag,default="") :
    return str(_cmd_dict.get(tag,default))

_parse()
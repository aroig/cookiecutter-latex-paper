
-- requires
lfs = require("lfs")

-- global state
userdata         = userdata or {}
userdata.state   = userdata.state or {}
userdata.revinfo = userdata.revinfo or {}

userdata.state.showcomments = false



local draftools={}


-- parses an active comment '%!' and returns the appropriate text
function draftools.parse_active_comments (line)

    -- If active comments is disabled, just return as it is.
    if not userdata.state.showcomments then
        return line
    end

    -- Process active comments beginning with "%!"
    local a,b,m,sp
    a,b,sp,m = string.find(line, "%s*%%!(%s*)(.*)")

    if not sp then sp = "" end
    local indent = string.len(sp)
    if indent > 0 then indent = indent - 1 end

    local space
    if indent > 0 then
        space = "\\hspace*{" .. tostring(indent/2.) .. "em}"
    else
        space = ""
    end

    if m then
        return "\\begincmt{}" .. space .. m .. "\\endcmt{}"
    else
        return line
    end
end



---------------------------------------------------------------------------
-- Revinfo                                                               --
---------------------------------------------------------------------------

-- default lib source
local INDEX = "INDEX"


-- checks whether working dir is clean
local function workingdir_clean()
    local out=io.popen('git status --porcelain', 'r')
    if out then
        local raw = out:read("*all"):gsub("^%s*(.-)%s*$", "%1")
        return string.len(raw) > 0
    else
        return false
    end
end


-- checks whether working dir is managed by git
local function is_git_repo()
    return lfs.attributes('.git', 'mode') == 'directory'
end


-- extract revision data from git
local function get_revision_data(rev)
    if rev == INDEX then gitrev = "HEAD"
    else gitrev = rev end

    local rd = {}
    local out=io.popen('git --no-pager log -1 --pretty="%h%n%H%n%an <%ae>%n%ai%n%s" ' .. gitrev, 'r')
    if out then
        local raw = out:read("*all")
        local t1,t2,t3,t4,t5 = raw:match("(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n")
        rd.shorthash = t1 or "unk"
        rd.hash = t2 or "unknown"
        rd.author = t3 or "???"
        rd.summary = t5 or ""

        if rev == INDEX then
            rd.clean = workingdir_clean()
            local outdate = io.popen('date --rfc-3339=seconds')
            t4 = outdate:read("*all")
        else
            rd.clean = true
        end

        if t4 then
            rd.date = t4:match("(%d+%-%d+%-%d+)")
            rd.time = t4:match("(%d+:%d+):%d+")
        else
            rd.date = "???"
            rd.time = "???"
        end

        return rd
    end
end


-- sets the workingdir revision
function draftools.set_workingdir_revinfo()
    userdata.state.diffmode = false
    userdata.revinfo = {}

    if is_git_repo() then
        userdata.revinfo.rev = get_revision_data(INDEX)
    end
end


-- sets the diff revision
function draftools.set_diff_revinfo(revA, revB)
    userdata.state.diffmode = true
    userdata.revinfo = {}

    if is_git_repo() then
        userdata.revinfo.revA = get_revision_data(revA)
        userdata.revinfo.revB = get_revision_data(revB)
    end
end


-- typesets revision information
function draftools.print_revinfo_header()
    if userdata.state.diffmode then
        local revA = userdata.revinfo.revA
        local revB = userdata.revinfo.revB

        local hashA = revA.shorthash
        if not revA.clean then hashA = hashA .. "+" end

        local hashB = revA.shorthash
        if not revB.clean then hashB = hashB .. "+" end


        tex.print(string.format("%s & %s %s & %s\\\\", hashA,
                                revA.date, revA.time, revA.summary))
        tex.print(string.format("%s & %s %s & %s\\\\", hashB,
                                revB.date, revB.time, revB.summary))
        return nil
    else
        local rev = userdata.revinfo.rev
        local hash = rev.shorthash
        if not rev.clean then hash = hash .. "+" end


        tex.print(string.format("%s & %s %s & %s", hash,
                                rev.date, rev.time, rev.summary))
    end
end



return draftools

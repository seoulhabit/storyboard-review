-- Single entry point, consolidating what were two separate icons
-- (New Storyboard.app + Validate Video.app) into one.
set toolChoice to choose from list {"Review clips (make a storyboard)", "Validate a video script"} with prompt "What do you want to do?" with title "Story Board" default items {"Review clips (make a storyboard)"}
if toolChoice is false then return -- Cancel
set toolChoice to item 1 of toolChoice

if toolChoice is "Review clips (make a storyboard)" then
	set proofPath to "/Users/sumitchoudhary/Desktop/Projects/SeoulHabit/seoulhabit-learn/video/proof"
	set storyboardLauncher to "/Users/sumitchoudhary/Desktop/Story Board/launcher.sh"

	-- Curated against video/scripts/regen-proof-frames.mjs's own manifest and
	-- video/design/component-registry.md's LIVE/RETIRED status — a proof/
	-- folder's NAME alone does not reliably say whether it's current (e.g.
	-- "depthofaction" is the RETIRED v1 archive; the real thing is
	-- "depthofaction-v2"). Live ones are listed first.
	set folderNames to {"brandmark", "clinicalcalendar", "conversionpath", "depthofaction-v2", "meters-v3", "pipette", "routeicon", "frameshell", "routineladder", "depthofaction", "flat-baseline", "hf3d", "ginseng", "retinal-vs-retinol"}
	set folderLabels to {"brandmark — live", "clinicalcalendar — live", "conversionpath — live", "depthofaction-v2 — live", "meters-v3 — live", "pipette — live", "routeicon — live", "frameshell — not wired into a video yet", "routineladder — not wired yet (v3 candidate)", "depthofaction — retired, see depthofaction-v2", "flat-baseline — reference only, not a component", "hf3d — reference only, not a component", "ginseng — ingredient reference frames", "retinal-vs-retinol — ingredient reference frames"}

	set choices to folderLabels & {"Other… (browse elsewhere)"}

	set pickedList to choose from list choices with prompt "Pick what to review:" with title "Story Board"
	if pickedList is false then return -- Cancel
	set pickedLabel to item 1 of pickedList

	if pickedLabel is "Other… (browse elsewhere)" then
		try
			set srcFolder to choose folder with prompt "Pick a folder of clips to review:" default location (POSIX file proofPath)
		on error number -128
			return
		end try
		set folderPath to POSIX path of srcFolder
	else
		set i to 0
		repeat with lbl in folderLabels
			set i to i + 1
			if lbl as text is pickedLabel then exit repeat
		end repeat
		set folderPath to proofPath & "/" & item i of folderNames
	end if

	display notification "Building storyboard…" with title "Story Board"

	try
		do shell script quoted form of storyboardLauncher & " " & quoted form of folderPath
	on error errText
		display alert "Couldn't build the storyboard" message "Something went wrong before the report could open. If you're not sure why, paste this into your next message to Claude:" & return & return & errText as critical
	end try

else
	set scriptsPath to "/Users/sumitchoudhary/Desktop/Projects/SeoulHabit/seoulhabit-learn/video/scripts"
	set storylineLauncher to "/Users/sumitchoudhary/Desktop/Story Board/launcher-storyline.sh"

	-- Reads video/scripts/*.json live each time — no live/retired ambiguity
	-- here the way proof/ folders have, so a plain dynamic listing is safe.
	-- The "| sort" means a zero-match ls's own failure never reaches AppleScript
	-- as a catchable error (the pipeline's exit status is sort's, not ls's) —
	-- confirmed directly against /bin/sh, do shell script's own runtime, not
	-- assumed — so this checks for empty output explicitly rather than relying
	-- on a try/on error that a real empty scripts/ folder would silently skip.
	try
		set fileListText to do shell script "cd " & quoted form of scriptsPath & " && ls -1 *.json | sort"
	on error
		set fileListText to ""
	end try
	if fileListText is "" then
		display alert "No scripts to validate yet" message "video/scripts/ doesn't have any .json files. Write one, then run this again."
		return
	end if
	-- "linefeed" is NOT a real AppleScript constant (confirmed directly: it
	-- silently evaluates to empty rather than raising an error) — but the
	-- real bug goes one step further: do shell script itself silently
	-- converts the shell's own LF-terminated output to CR when handing it
	-- back to AppleScript (confirmed by inspecting the actual character
	-- code at a line boundary: 13, not 10). So even "ASCII character 10"
	-- would still be wrong here — AppleScript's own "return" (CR) is the
	-- delimiter that actually matches what do shell script hands back.
	set AppleScript's text item delimiters to return
	set scriptFiles to text items of fileListText
	set AppleScript's text item delimiters to ""

	set pickedList2 to choose from list scriptFiles with prompt "Pick a script to validate:" with title "Story Board"
	if pickedList2 is false then return -- Cancel
	set pickedName to item 1 of pickedList2

	set scriptPath to scriptsPath & "/" & pickedName

	try
		do shell script quoted form of storylineLauncher & " " & quoted form of scriptPath
	on error errText
		display alert "Couldn't validate the script" message "Something went wrong before the report could open. If you're not sure why, paste this into your next message to Claude:" & return & return & errText as critical
	end try
end if

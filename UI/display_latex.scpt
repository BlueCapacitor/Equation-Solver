set equationFile to (open for access "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output.txt")
set equation to (read equationFile)

tell application "LaTeXiT" to activate
tell application "System Events" to tell process "LaTeXiT"
	key code 51 using {command down}
	keystroke equation
	keystroke "t" using {command down}
end tell
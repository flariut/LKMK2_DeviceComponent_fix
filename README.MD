# Launchkey 25, 49, 61 MK2 - Device Parameter Banks not available for VST/Plugins FIX

On Ableton Live you can't select any Device Parameter Bank other than the first with third party plugins, and the root of this issue is a bug in Launchkey MK2's MIDI Remote Script. The bug is annoying because the pink lights of the banks glow as available, but you just can't select them, and if you wan't to manually tweak, for example, various Synth parameters, you simply can't more than 8.

After contacting Novation a few months ago and not getting a definitive answer from their end, and taking advantage of the free time offered by the quarantine due to COVID-19, I decided to take action on the matter.

For you people that understand anything of Python and Ableton's MIDI Remote Scripts, this was the root of the issue: Line 64 of the file "DeviceComponent.py" (https://github.com/gluon/AbletonLive10.1_MIDIRemoteScripts/blob/master/Launchkey_MK2/DeviceComponent.py) created a kind of infinite loop by referencing the method "\_number\_of\_parameter\_banks" of the child class "DeviceComponent", but actually it had to do a reference to the method of parent class  "DeviceComponentBase". The problem wasn't crashing completely Live thanks to Python's maximum recursion depth RecursionError. By simply changing that line, the behavior of the Launchkey MK2 is as expected.

I will share the following steps for easily fixing the bug if it's a functionality you need.

**NOTICE: THIS IS NOT OFFICIALLY SUPPORTED NEITHER BY ABLETON OR NOVATION UNTIL IT EVENTUALLY GETS FIXED ON A RELEASE, SO DO IT AT YOUR OWN RISK**

**Steps:**

1. Download modified **"DeviceComponent.py"** from this repository
2. Place it in: macOS, **"/Applications/Ableton Live x.x.x.app/Contents/App-Resources/MIDI Remote Scripts/Launchkey\_MK2"** or Windows, **"C:\\Program Files\\Ableton\\Live x.x.x\\Resources\\MIDI Remote Scripts\\Launchkey\_MK2"**
3. Remove existing **"DeviceComponent.pyc"**
4. Run Live
5. A new "DeviceComponent.pyc" should appear. Then you can delete "DeviceComponent.py"
6. Enjoy tweaking parameters

from PIL import Image

# 1. Push 1: red -> dark red (Hue 0, Lightness +2 = Pop wait, push is Hue 0, Lightness +1)
# Light Red is (255, 192, 192)
# Normal Red is (255, 0, 0)
# Dark Red is (192, 0, 0)
# Light Red -> Normal Red = (Hue 0, Lightness 1) -> push
# Size 2 -> push 2

width = 4
height = 1
img = Image.new("RGB", (width, height))
pixels = img.load()

# Block 1: Light Red (size 2) -> Push 2
pixels[0,0] = (255, 192, 192)
pixels[1,0] = (255, 192, 192)

# Block 2: Normal Red (size 1) -> push triggers? Light Red -> Normal Red is lightness+1, Hue+0
pixels[2,0] = (255, 0, 0)

# Block 3: Dark Yellow (size 1) -> Normal Red -> Dark Yellow
# Normal Red = (0, 1). Dark Yellow = (1, 2)
# Hue change: 1. Lightness change: 1.
# (1, 1) -> subtract. Wait, out(number) is (5, 1).
# Need to go from Normal Red (0, 1) to Magenta (5, 2) -> Hue diff 5, Lightness diff 1
# Normal Magenta is (255, 0, 255) -> (5, 1).
# Dark Magenta is (192, 0, 192) -> (5, 2).
# Normal Red(0,1) -> Dark Magenta(5,2): Hue diff 5, Lightness diff 1 -> out(number)!
pixels[3,0] = (192, 0, 192)

img.save("simple.png")

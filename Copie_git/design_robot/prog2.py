
from svgwrite import Drawing

# Dimensions
width = 300  # 30 cm in mm
height = 300  # 30 cm in mm
thickness = 3  # 3 mm



# Create new SVG with the updated specifications
dwg = Drawing('robot_flame_base.svg', size=(width, height))

# Dimensions for the front rectangle
rect_length = 150  # 15 cm in mm
rect_width = 100   # 10 cm in mm

# Draw the rectangle for motors and wheels at the front
motor_rect = dwg.rect(insert=(0, (height - rect_width) / 2), size=(rect_length, rect_width), fill='none', stroke='black', stroke_width=1)
dwg.add(motor_rect)

# Draw the flame starting from the right side of the rectangle, extending by 15 cm in width
flame_length = 150  # 15 cm in mm
flame_height = rect_width

# Create flame shape (abstract, wavy lines)
flame_path = dwg.path(d=("M{} {} C{} {}, {} {}, {} {}".format(
        rect_length, (height - rect_width) / 2,  # Start at the top-right corner of the rectangle
            rect_length + flame_length * 0.33, (height - rect_width) / 2 - flame_height * 0.2,  # Curve 1
                rect_length + flame_length * 0.66, (height + rect_width) / 2 + flame_height * 0.2,  # Curve 2
                    rect_length + flame_length, (height - rect_width) / 2  # End at the far-right, aligning with the rectangle
                    )), fill='none', stroke='black', stroke_width=1)

# Add flame to the drawing
dwg.add(flame_path)

# Save the updated SVG
dwg.save()
'/mnt/data/robot_flame_base.svg'






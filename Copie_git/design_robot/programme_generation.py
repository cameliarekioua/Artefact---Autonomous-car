from svgwrite import Drawing

# Dimensions
width = 300  # 30 cm in mm
height = 300  # 30 cm in mm
thickness = 3  # 3 mm

# Create SVG drawing
dwg = Drawing('robot_base.svg', size=(width, height))

# Draw rectangle for motors and wheels at the front (30% of the total height)
motor_rect_height = height * 0.3
motor_rect = dwg.rect(insert=(0, 0), size=(width, motor_rect_height), fill='none', stroke='black', stroke_width=1)
dwg.add(motor_rect)

# Draw the flame design on the rear part (70% of the total height)
flame_points = [
    (width*0.15, motor_rect_height), (width*0.25, motor_rect_height + 10), (width*0.35, motor_rect_height - 5),
    (width*0.45, motor_rect_height + 15), (width*0.55, motor_rect_height), (width*0.65, motor_rect_height + 10),
    (width*0.75, motor_rect_height - 5), (width*0.85, motor_rect_height + 15), (width, motor_rect_height)
]
flame_polygon = dwg.polygon(points=flame_points, fill='red', stroke='black', stroke_width=1)
dwg.add(flame_polygon)

# Add multiple flames along the rear part
for i in range(5):
    flame_x_offset = i * (width / 5)
    flame_points = [
        (flame_x_offset + width*0.05, motor_rect_height + 10), 
        (flame_x_offset + width*0.1, motor_rect_height + 30), 
        (flame_x_offset + width*0.15, motor_rect_height + 10),
        (flame_x_offset + width*0.1, motor_rect_height)
    ]
    small_flame_polygon = dwg.polygon(points=flame_points, fill='orange', stroke='black', stroke_width=1)
    dwg.add(small_flame_polygon)

# Save the SVG file
dwg.save()
'/mnt/data/robot_base.svg'


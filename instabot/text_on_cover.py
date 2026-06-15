from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont

def text_on_cover(video_path, text):
    """
    Extracts a frame from the video, applies a wrapped text overlay over a 
    semi-transparent white background box, and saves it as a JPEG thumbnail cover.

    Args:
        video_path (str): The absolute or relative path to the target MP4 video file.
        text (str): The main title/heading text to write on the cover image.

    Returns:
        bool: True on successful thumbnail generation, False otherwise.
    """
    try:
        if text != "":
            from constants import cover_font_path

            # Load the video using a context manager to ensure safe OS descriptor release
            with VideoFileClip(video_path) as video:
                # Calculate dynamic font size matching video dimensions and aspect ratio
                video_width, video_height = video.size
                aspect_ratio = video_width / video_height
                fontsize = int(video_height * (0.035 + 0.02 * aspect_ratio))

                # Extract a single frame at exactly 1/5 of the video duration
                frame = video.get_frame(video.duration / 5)

            # Convert frame NumPy array into a PIL image supporting RGBA layer composition
            image = Image.fromarray(frame).convert("RGBA")
            draw = ImageDraw.Draw(image)

            # Safely load the designated font or fallback to the system default
            try:
                font = ImageFont.truetype(cover_font_path, size=fontsize)
            except IOError:
                font = ImageFont.load_default()

            # Helper inner function to dynamically wrap text lines to fit inside margins
            def break_text_to_lines(input_text, current_font, text_limit_width):
                lines = []
                words = input_text.split()
                if not words:
                    return lines

                current_line = words[0]
                for word in words[1:]:
                    bbox = draw.textbbox((0, 0), current_line + " " + word, font=current_font)
                    width = bbox[2] - bbox[0]
                    if width <= text_limit_width:
                        current_line += " " + word
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
                return lines

            # Assign maximum text box boundary width depending on layout orientation
            if image.width < image.height:
                max_width = int(image.width * 0.7)
            else:
                max_width = int(image.width * 0.3)

            lines = break_text_to_lines(text, font, max_width)

            # Calculate cumulative vertical height of wrapped lines including padding
            line_spacing = 5
            total_text_height = sum(
                [
                    draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
                    for line in lines
                ]
            ) + (len(lines) - 1) * line_spacing

            # Create a semi-transparent RGBA overlay layer for the background shape
            overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)

            # White background color with ~88% opacity (224 / 255)
            background_color = (255, 255, 255, 224)
            padding = fontsize / 2
            
            max_line_width = max(
                [
                    draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
                    for line in lines
                ]
            )

            # Center text coordinates vertically and horizontally
            y_offset = ((image.height - total_text_height) // 2) - padding
            background_x0 = (image.width - max_line_width - 2 * padding) // 2
            background_y0 = y_offset
            background_x1 = background_x0 + max_line_width + 2 * padding
            background_y1 = background_y0 + total_text_height + 2 * padding

            # Render the background block onto the transparent overlay layer
            overlay_draw.rectangle([background_x0, background_y0, background_x1, background_y1], fill=background_color)

            # Composite frame background with the overlay layer
            image = Image.alpha_composite(image, overlay)

            # Draw final wrapped texts over the composited layer
            final_draw = ImageDraw.Draw(image)
            for line in lines:
                text_width, text_height = final_draw.textbbox((0, 0), line, font=font)[2:4]
                x_position = (image.width - text_width) // 2

                # Render text in safe dark-grey color (RGB: 35, 35, 35)
                final_draw.text((x_position, y_offset), line, font=font, fill=(35, 35, 35))
                y_offset += text_height + line_spacing

            # Export RGBA layers to a flat RGB file and save as JPEG cover asset
            rgb_image = image.convert("RGB")
            thumbnail_path = f"{video_path}.jpg"
            rgb_image.save(thumbnail_path)
            return True
        else:
            return True
        
    except Exception:
        return False
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from bidi.algorithm import get_display
import arabic_reshaper

def text_on_video(video_path, top_text, username):
    """
    Renders top title texts and bottom call-to-action bars directly onto video clips.
    Uses dynamic reshaping and bidirectional layouts to display Persian RTL text formats correctly.

    Args:
        video_path (str): Path to the target source MP4 video file.
        top_text (str): The main title/heading text written at the top of the video.
        username (str): Instagram profile handle (username).

    Returns:
        bool: True if editing completes successfully and output is generated, False otherwise.
    """
    try:
        from constants import call_to_action, video_font_path, english_pages, english_call_to_action

        tmp_output = "./tmp_output.mp4"
        tmp_output_temp_snd = "./tmp_outputTEMP_MPY_wvf_snd.mp4"

        # Safely purge existing temporary artifacts on storage to avoid permission conflicts
        if os.path.exists(tmp_output):
            os.remove(tmp_output)

        if os.path.exists(tmp_output_temp_snd):
            os.remove(tmp_output_temp_snd)

        if not os.path.exists(video_font_path):
            return False

        # Helper function to dynamically split text lines without breaking raw words
        def wrap_text(text_string, word_limit):
            words = text_string.split()
            lines = []
            current_line = ""

            for word in words:
                if len(current_line + word) <= word_limit:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip())

            return lines

        # Load video within a context manager block to prevent process execution lockups
        with VideoFileClip(video_path) as video:
            video_width, video_height = video.size

            # Dynamic font scale sizing matching target video dimensions
            fontsize = int(video_height * 0.04)
            max_width = int(video_width * 2 / fontsize)

            # ------------------------------------------------------------------------------
            # Case A: English Target Profiles (Skip Arabic shaping and Bidi processing)
            # ------------------------------------------------------------------------------
            if username in english_pages:
                share_and_username = f"{english_call_to_action}\n@{username}"

                share_and_username_clip = TextClip(
                    share_and_username,
                    fontsize=fontsize,
                    font=video_font_path,
                    color="white",
                    bg_color="rgba(0, 0, 0, 0.5)"
                ).set_position(("center", int(video_height * 0.89) - fontsize)).set_duration(video.duration)

                if top_text != "":
                    wrapped_top_lines = wrap_text(top_text, word_limit=max_width)
                    final_top_text = "\n".join(wrapped_top_lines)

                    top_text_clip = TextClip(
                        final_top_text,
                        fontsize=fontsize,
                        font=video_font_path,
                        color="white",
                        bg_color="rgba(0, 0, 0, 0.5)"
                    ).set_position(("center", int(video_height * 0.06))).set_duration(video.duration)

                    # Compile and write modified video clip
                    with CompositeVideoClip([video, top_text_clip, share_and_username_clip]) as final_video:
                        final_video.write_videofile(tmp_output, codec="libx264", audio_codec="aac")
                else:
                    # Compile modified video with only bottom banners
                    with CompositeVideoClip([video, share_and_username_clip]) as final_video:
                        final_video.write_videofile(tmp_output, codec="libx264", audio_codec="aac")

            # ------------------------------------------------------------------------------
            # Case B: Persian Target Profiles (Enable reshaper and bidirectional engines)
            # ------------------------------------------------------------------------------
            else:
                share_and_username = f"{call_to_action}\n{username}@"

                # Shape and align Persian banners
                reshaped_share_and_username = arabic_reshaper.reshape(share_and_username)
                display_share_and_username = get_display(reshaped_share_and_username)

                share_and_username_clip = TextClip(
                    display_share_and_username,
                    fontsize=fontsize,
                    font=video_font_path,
                    color="white",
                    bg_color="rgba(0, 0, 0, 0.5)"
                ).set_position(("center", int(video_height * 0.89) - fontsize)).set_duration(video.duration)

                if top_text != "":
                    # Shape and align Persian titles
                    reshaped_top_text = arabic_reshaper.reshape(top_text)
                    display_top_text = get_display(reshaped_top_text)
                    wrapped_top_lines = wrap_text(display_top_text, word_limit=max_width)
                    
                    # Reverse mapped lines order to secure standard Persian sequence
                    final_top_text = "\n".join(reversed(wrapped_top_lines))

                    top_text_clip = TextClip(
                        final_top_text,
                        fontsize=fontsize,
                        font=video_font_path,
                        color="white",
                        bg_color="rgba(0, 0, 0, 0.5)"
                    ).set_position(("center", int(video_height * 0.06))).set_duration(video.duration)

                    # Compile and write modified video clip
                    with CompositeVideoClip([video, top_text_clip, share_and_username_clip]) as final_video:
                        final_video.write_videofile(tmp_output, codec="libx264", audio_codec="aac")
                else:
                    # Compile modified video with only bottom banners
                    with CompositeVideoClip([video, share_and_username_clip]) as final_video:
                        final_video.write_videofile(tmp_output, codec="libx264", audio_codec="aac")

        # Safely convert output and replace file with temp indicators
        tmp_video_path = video_path.replace('.mp4', '-tmp.mp4')
        if os.path.exists(tmp_output):
            os.rename(tmp_output, tmp_video_path)
            return True
        return False

    except Exception:
        return False
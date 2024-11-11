from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips, vfx, TextClip, CompositeVideoClip

class VideoProcessor:
    def __init__(self, file_path):
        # 加载视频文件
        self.video = VideoFileClip(file_path)
    
    def mute_volume(self):
        """
        调整音量
        """
        self.video = self.video.without_audio()
        return self

    def change_volume(self, volume_factor):
        """
        调整音量
        volume_factor: 音量倍数（1.0 为原始音量，小于 1.0 减小音量，大于 1.0 增大音量）
        """
        self.video = self.video.volumex(volume_factor)
        return self

    def change_speed(self, speed=1.0):
        """
        改变播放速度
        speed: 播放速度倍率。1.0 为原速，小于 1.0 放慢，大于 1.0 加快
        """
        self.video = self.video.fx(vfx.speedx, speed)
        return self
    
    def resize(self, new_size):
        """
        调整视频大小
        new_size: 新的尺寸倍率，例如 0.5 表示缩小一半，2 表示放大一倍
        """
        self.video = self.video.resize(new_size)
        return self
    
    def fadein(self, duration):
        """
        添加淡入效果
        duration: 淡入效果的持续时间，以秒为单位
        """
        self.video = self.video.fadein(duration)
        return self
    
    def fadeout(self, duration):
        """
        添加淡出效果
        duration: 淡出效果的持续时间，以秒为单位
        """
        self.video = self.video.fadeout(duration)
        return self

    def add_audio(self, audio_path, start_time=0, volume=1.0):
        """
        增加音频到视频
        audio_path: 音频文件路径
        start_time: 音频开始播放的时间（以秒为单位）
        volume: 音频音量倍率，1.0 为原始音量
        """
        audio = AudioFileClip(audio_path).volumex(volume)
        audio = audio.set_start(start_time).set_duration(self.video.duration)
        self.video = self.video.set_audio(audio)
        return self

    def add_image(self, image_path, position=('center', 'bottom')):        
        w, h = self.video.size
        clip = ImageClip(image_path, duration=self.video.duration).set_position(position)
     #   clip = clip.fx(vfx.resize, (w-40, h//3))
        self.video = CompositeVideoClip([self.video, clip])
        return self
            
    def mix_with(self, another_video_path, volume_balance=0.5):
        """
        混合视频的音频
        another_video_path: 另一个视频文件的路径，与当前视频文件的音频混合
        volume_balance: 另一视频的音频混合音量比例（0 到 1 之间，0.5 为两者平衡，1 为另一视频全音量）
        """
        another_video = VideoFileClip(another_video_path).volumex(volume_balance)
        audio = another_video.audio
        audio.set_duration(self.video.duration)
        self.video = self.video.set_audio(audio)
 #       self.video = self.video.set_audio(self.video.audio.overlay(another_video.audio))
        return self
    
    def trim(self, start_time, end_time):
        """
        裁剪视频
        start_time: 裁剪起始位置，以秒为单位
        end_time: 裁剪结束位置，以秒为单位
        """
        self.video = self.video.subclip(start_time, end_time)
        return self
    
    def trim_multiple_clips(self, clip_times):
        """
        从视频中裁剪多个片段并合并
        clip_times: 包含 (start, end) 元组列表的片段时间
                    [(8, 35), (51, 70)]
        """
        clips = [self.video.subclip(start, end) for start, end in clip_times]
        self.video = concatenate_videoclips(clips)
        return self
    
    def concatenate(self, another_video_path):
        """
        拼接视频文件
        another_video_path: 另一个视频文件的路径，将在当前视频文件的末尾拼接
        """
        another_video = VideoFileClip(another_video_path)       
        self.video = concatenate_videoclips([self.video, another_video])
        return self

    def concatenate_multiple_clips(self, another_video_path, clip_times):
        """
        拼接视频文件
        another_video_path: 另一个视频文件的路径，将在当前视频文件的末尾拼接
                clip_times: 包含 (start, end) 元组列表的片段时间
                    [(8, 35), (51, 70)]
        """
        another_video = VideoFileClip(another_video_path)
        clips = [another_video.subclip(start, end) for start, end in clip_times]
#        lst = []
#        lst.append(self.video)
#        lst.extend(clips)
#        self.video = concatenate_videoclips(lst)
        self.video = concatenate_videoclips([self.video]+clips)
        return self
    

    def add_text(self, text, fontsize=24, color='white', position=('center', 'bottom'), duration=None):
        """
        添加文本到视频
        text: 显示的文本内容
        fontsize: 字体大小
        color: 文本颜色
        position: 文本位置，例如 ('center', 'top')
        duration: 文本显示时长，默认为整个视频时长
        """
        duration = duration or self.video.duration
        text_clip = TextClip(text, fontsize=fontsize, color=color).set_position(position).set_duration(duration)
        self.video = CompositeVideoClip([self.video, text_clip])
        return self
    
    def export(self, output_path):
        """
        导出视频文件
        output_path: 导出文件的路径
        """
        self.video.write_videofile(output_path)
        print(f"视频已导出到 {output_path}")

    def export_audio(self, output_path):
        """
        导出视频文件
        output_path: 导出文件的路径
        """
        self.video.audio.write_audiofile(output_path)
        print(f"音频已导出到 {output_path}")
        

   
def test1():
    processor = VideoProcessor("input.mp4")
    
    # 调整音量（增加 1.5 倍）
    processor.change_volume(1.5)
    
    # 拼接另一个视频文件
    processor.concatenate("another_input.mp4")
    
    # 混合音频，另一视频音量为 0.5 倍
    processor.mix_with("background.mp4", volume_balance=0.5)
    
    # 裁剪视频（从 1 秒到 5 秒）
    processor.trim(1, 5)
    
    # 改变播放速度（加快 1.5 倍）
    processor.change_speed(1.5)
    
    # 调整视频大小（缩小为原来的一半）
    processor.resize(0.5)
    
    # 添加淡入和淡出效果（2 秒）
    processor.fadein(2).fadeout(2)
    
    # 添加文本 "Hello, MoviePy!" 显示在视频底部，持续 3 秒
    processor.add_text("Hello, MoviePy!", fontsize=30, color='yellow', position=('center', 'bottom'), duration=3)
    
    # 导出结果
    processor.export("output.mp4")


def test2():
    input_path = "C:\\chrome\\test\\"
    output_path = "C:\\chrome\\test\\"

    v1_path = str(input_path + "dji_1.mp4")
    mix_1_path = str(input_path + "m1.mp3")
    
    out_1_path = str(output_path + "o1.mp4")
    
    processor = VideoProcessor(v1_path)
    

    # 裁剪视频中多个片段并合并
    # 例如，裁剪出从 1 到 3 秒和从 5 到 7 秒的两个片段并拼接
#    processor.trim_multiple_clips([(8, 35), (51, 70)])
    processor.trim_multiple_clips([(8, 15), (51, 60)])
        
    # 增加背景音频，从视频的第 2 秒开始，音量为 0.8 倍
    processor.add_audio(mix_1_path, start_time=2, volume=0.3)
    

    # 添加淡入和淡出效果（2 秒）
    processor.fadein(3).fadeout(3)
    
    # 添加文本 "加油，根号一班!" 显示在视频底部，持续 3 秒
#    processor.add_text("Hello, MoviePy!", fontsize=30, color='yellow', position=('center', 'bottom'), duration=30)
    
    # 调整视频大小（缩小为原来的一半）
#    processor.resize(0.5)
    
    processor.add_image("C:\\chrome\\test\\image.png")
    
    # 导出结果
    processor.export("C:\\chrome\\test\\o2.mp4")
    

def test3():
    input_path = "C:\\chrome\\test\\"
    output_path = "C:\\chrome\\test\\"

    v1_path = str(input_path + "dji_1.mp4")
    background_voice_path = str(input_path + "m1.mp3")
    mix_voice_path = str(input_path + "mobile_1.mp4")
    
    out_1_path = str(output_path + "o11.mp4")
    
    processor = VideoProcessor(v1_path)
    
    # 混合音频，另一视频音量为 0.5 倍
    processor.mix_with(mix_voice_path, 1)

    # 裁剪视频中多个片段并合并
    # 例如，裁剪出从 1 到 3 秒和从 5 到 7 秒的两个片段并拼接
    processor.trim_multiple_clips([(5, 35), (51, 70)])
        
#    processor.concatenate_multiple_clips('C:\\chrome\\test\\o2.mp4', [(1, 5), (8, 13)])
    
    # 增加背景音频，从视频的第 2 秒开始，音量为 0.8 倍
    processor.add_audio(mix_voice_path, start_time=2, volume=0.5)
    

    # 添加淡入和淡出效果（2 秒）
    processor.fadein(1).fadeout(1)
    

    processor.add_image("C:\\chrome\\test\\801.png")
    
    # 导出结果
    processor.export("C:\\chrome\\test\\11.mp4")
    


# 示例用法
if __name__ == "__main__":   
    test3()
        
    


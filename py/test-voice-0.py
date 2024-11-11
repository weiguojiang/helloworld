from moviepy.editor import AudioFileClip, concatenate_audioclips

class AudioProcessor:
    def __init__(self, file_path):
        # 加载音频文件
        self.audio = AudioFileClip(file_path)
    
    def change_volume(self, volume_factor):
        """
        调整音量
        volume_factor: 音量倍数（1.0 为原始音量，小于 1.0 减小音量，大于 1.0 增大音量）
        """
        self.audio = self.audio.volumex(volume_factor)
        return self

    def fadein(self, duration):
        """
        添加淡入效果
        duration: 淡入效果的持续时间，以秒为单位
        """
        self.audio = self.audio.audio_fadein(duration)
        return self
    
    def fadeout(self, duration):
        """
        添加淡出效果
        duration: 淡出效果的持续时间，以秒为单位
        """
        self.audio = self.audio.audio_fadein(duration)
        return self
    
    def concatenate(self, another_audio_path):
        """
        拼接音频文件
        another_audio_path: 另一个音频文件的路径，将在当前音频文件的末尾拼接
        """
        another_audio = AudioFileClip(another_audio_path)
        self.audio = concatenate_audioclips([self.audio, another_audio])
        return self
    
    def concatenate_clips(self, clip_paths):
        """
        拼接多个音频片段
        clip_paths: 包含要拼接的音频文件路径列表
        """
        clips = [AudioFileClip(path) for path in clip_paths]
        self.audio = concatenate_audioclips([self.audio] + clips)
        return self
    
    def mix_with(self, another_audio_path, volume_balance=0.5):
        """
        混合音频文件
        another_audio_path: 另一个音频文件的路径，与当前音频文件进行混音
        volume_balance: 另一音频文件的混合音量比例（0 到 1 之间，0.5 为两者平衡，1 为另一音频全音量）
        """
        another_audio = AudioFileClip(another_audio_path).volumex(volume_balance)
        self.audio = self.audio.set_duration(max(self.audio.duration, another_audio.duration))
        self.audio = self.audio.audio_fadein(100).audio_fadeout(100)
        self.audio = self.audio.overlay(another_audio)
        return self

    def trim(self, start_time, end_time):
        """
        裁剪音频
        start_time: 裁剪起始位置，以秒为单位
        end_time: 裁剪结束位置，以秒为单位
        """
        self.audio = self.audio.subclip(start_time, end_time)
        return self

    def trim_multiple_clips(self, clip_times):
        """
        从音频中裁剪多个片段并拼接
        clip_times: 包含 (start, end) 元组列表的片段时间
        """
        clips = [self.audio.subclip(start, end) for start, end in clip_times]
        self.audio = concatenate_audioclips(clips)
        return self

    def change_speed(self, speed=1.0):
        """
        改变播放速度
        speed: 播放速度倍率。1.0 为原速，小于 1.0 放慢，大于 1.0 加快
        """
        self.audio = self.audio.fx(vfx.speedx, speed)
        return self
    
    def export(self, output_path):
        """
        导出音频文件
        output_path: 导出文件的路径
        """
        self.audio.write_audiofile(output_path)
        print(f"音频已导出到 {output_path}")

if __name__ == "__main__":
    processor = AudioProcessor("input.mp3")
    
    # 调整音量（增加 1.5 倍）
    processor.change_volume(1.5)
    
    # 拼接其他音频片段
    processor.concatenate_clips(["clip1.mp3", "clip2.mp3"])
    
    # 混合另一个音频，并将另一音频音量设置为 0.5 倍
    processor.mix_with("background.mp3", volume_balance=0.5)
    
    # 裁剪多个音频片段并拼接，例如从 5 秒到 10 秒和从 15 秒到 20 秒的片段
    processor.trim_multiple_clips([(5, 10), (15, 20)])
    
    # 改变播放速度（加快 1.2 倍）
    processor.change_speed(1.2)
    
    # 导出结果
    processor.export("output.mp3")
    

from pydub import AudioSegment

#功能解释
#音量调整：change_volume 方法通过音量倍数（volume_factor）调节音频音量。
#音频拼接：concatenate_clips 方法支持传入多个音频片段的路径列表，将它们拼接成一个完整的音频。
#音频混音：mix_with 方法将另一个音频文件与当前音频混合，volume_balance 控制另一音频的音量比例。
#多片段裁剪：trim_multiple_clips 方法可以从音频中裁剪多个片段，并将它们拼接成一个新的音频。
#改变播放速度：change_speed 方法通过倍速参数调整播放速度。
#导出：export 方法将处理完成的音频导出为指定文件。


class AudioProcessor:
    def __init__(self, file_path):
        # 加载音频文件
        self.audio = AudioSegment.from_file(file_path)
    
    def change_volume(self, db_change):
        """
        调整音量
        db_change: 增加或减少的分贝数，正值增大音量，负值减小音量
        """
        self.audio = self.audio + db_change
        return self
    
    def concatenate(self, another_audio_path):
        """
        拼接音频文件
        another_audio_path: 另一个音频文件的路径，将在当前音频文件的末尾拼接
        """
        another_audio = AudioSegment.from_file(another_audio_path)
        self.audio = self.audio + another_audio
        return self
    
    def concatenate_clips(self, clip_paths):
        """
        拼接多个音频片段
        clip_paths: 包含要拼接的音频文件路径列表
        """
        clips = [AudioSegment.from_file(path) for path in clip_paths]
        self.audio = sum([self.audio] + clips)
        return self
    
    
    def mix_with(self, another_audio_path, volume_balance=0, position=0, loop=False, times=None, gain_during_overlay=None):
        """
        混合音频文件
        another_audio_path: 另一个音频文件的路径，与当前音频文件进行混音
        volume_balance: 设置混音平衡，负值减小 another_audio 的音量，正值增大 another_audio 的音量
        """
        another_audio = AudioSegment.from_file(another_audio_path)
        another_audio = another_audio + volume_balance  # 调整另一音频文件的音量
        self.audio = self.audio.overlay(another_audio, position, loop, times, gain_during_overlay)
        return self

    def trim(self, start_ms, end_ms):
        """
        裁剪音频
        start_ms: 裁剪起始位置，以毫秒为单位
        end_ms: 裁剪结束位置，以毫秒为单位
        """
        self.audio = self.audio[start_ms:end_ms]
        return self
    
    def trim_multiple_clips(self, clip_times):
        """
        从音频中裁剪多个片段并拼接
        clip_times: 包含 (start, end) 元组列表的片段时间，以毫秒为单位
        """
        clips = [self.audio[start:end] for start, end in clip_times]
        self.audio = sum(clips)
        return self
    
    def change_speed(self, speed=1.0):
        """
        改变播放速度
        speed: 播放速度倍率。1.0 为原速，小于 1.0 放慢，大于 1.0 加快
        """
        new_frame_rate = int(self.audio.frame_rate * speed)
        self.audio = self.audio._spawn(self.audio.raw_data, overrides={'frame_rate': new_frame_rate})
        self.audio = self.audio.set_frame_rate(44100)  # 调整回标准的采样率
        return self
    
    def export(self, output_path, format="wav"):
        """
        导出音频文件
        output_path: 导出文件的路径
        format: 导出文件的格式，默认为 wav
        """
        self.audio.export(output_path, format=format)
        print(f"音频已导出到 {output_path}，格式为 {format}")

def test_example():
    processor = AudioProcessor("input.mp3")
    
    # 调整音量（增加 6 分贝）
    processor.change_volume(6)
    
    # 拼接其他音频片段
    processor.concatenate_clips(["clip1.mp3", "clip2.mp3"])
    
    # 混合另一个音频，将另一音频音量调整为 0.5
    processor.mix_with("background.mp3", volume_balance=0.5)
    
    # 裁剪多个音频片段并拼接，例如裁剪 5 到 10 秒和 15 到 20 秒的片段
    processor.trim_multiple_clips([(5000, 10000), (15000, 20000)])
    
    # 改变播放速度（加快 1.2 倍）
    processor.change_speed(1.2)
    
    # 导出结果
    processor.export("output.mp3")
    

def test_kk():
    input_path = "C:\\chrome\\in\\"
    output_path = "C:\\chrome\\test\\"

    v1_path = str(input_path + "1.MOV")
    plus_1_path = str(input_path + "2.mp3")

    mix_1_path = str(output_path + "m1.mp3")
    
    out_1_path = str(output_path + "o1.mp3")

    processor = AudioProcessor(v1_path)
    
    # 调整音量（+5 分贝）
    processor.change_volume(1.1)
    
    # 拼接另一个音频文件
#    processor.concatenate(plus_1_path)
    
    # 与另一个音频文件混音，并将其音量减小 5 分贝
    processor.mix_with(mix_1_path, volume_balance=-5)
    
    # 裁剪音频（从1秒到5秒）
#    processor.trim(1000, 80000)
    
    # 改变播放速度（加快 1.5 倍）
    processor.change_speed(0.8)
    
    # 导出结果
    processor.export(out_1_path, 'mp3')

import sys,os
    
# 示例用法
if __name__ == "__main__":
#    sys.path.append(r'C:\chrome\test')
#    os.chdir(r'C:/chrome/test')

    test_kk()
    

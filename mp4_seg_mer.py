#该代码用于mp4视频文件的分割与合并

import subprocess
import os



'''------------------------------------------视频切分代码------------------------------------------'''
def get_video_duration(input_file):
    """
    获取视频的时长
    :param input_file: 输入的MP4文件路径
    :return: 视频时长（单位：秒）
    """
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    duration = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
    duration = float(duration.strip())
    return duration


def split_video(input_file, output_dir, segment_duration):
    """
    按时间切分MP4文件
    :param input_file: 输入的MP4文件路径
    :param output_dir: 输出的文件夹路径
    :param segment_duration: 每个切分视频的时长（单位：秒）
    :return: None
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取视频时长
    video_duration = get_video_duration(input_file)

    # 计算需要切分的视频段数
    num_segments = int(video_duration / segment_duration) + 1
    
    # 切分视频
    for i in range(num_segments):
        # 计算当前切分视频的起始时间和结束时间
        segment_start_time = i * segment_duration
        segment_end_time = min(segment_start_time + segment_duration, video_duration)
        
        # 构造输出文件名
        output_file = os.path.join(output_dir, f'segment_{i}.mp4')
        
        # 构造FFmpeg命令
        command = ['ffmpeg', '-i', input_file, '-ss', str(segment_start_time), '-to', str(segment_end_time), '-c:v', 'libx264', '-c:a', 'aac','-map', '0:v', '-map', '0:a', output_file]
        #参数说明：'-ss'：切分子视频的开始时间；'-to'：切分子视频的结束时间；'-c:v'：视频编码器，强制将视频从一种编码格式转换成另一种，这里将视频转换成H.264编码，不这样做的话会出现画面缺失
        #         '-c:a'：音频编码器，将视频中的音频统一编码为acc格式；'-map'：视频/音频流提取，指定提取哪个流，这里提取全部流

        # 执行FFmpeg命令
        subprocess.call(command)
'''------------------------------------------视频切分代码------------------------------------------'''

 # 分支改的


'''------------------------------------------视频合并代码------------------------------------------'''
def conver_videos(input_file_name, intput_dir, temp_dir):
    """
    将mp4文件统一格式并转换成ts格式的中间文件
    :param input_file_name: 输入的MP4文件的文件名（不是路径）
    :param intput_dir: 输入的mp4文件的存放目录
    :param temp_dir: 转换好的中间文件的存放目录
    :return: 中间文件路径列表
    """
    temp_files = []
    for mp4_file in input_file_name:
        input_file = os.path.join(intput_dir, mp4_file)        #mp4文件地址

        temp_file_name = mp4_file.split(".")[0]+".ts"
        temp_file = os.path.join(temp_dir, temp_file_name)     #ts格式的中间文件的存放地址
        temp_files.append(temp_file)

        command = ['ffmpeg', '-i', input_file, '-vcodec', 'copy', '-acodec', 'copy', '-vbsf', 'h264_mp4toannexb', temp_file]    #将mp4文件转换成ts文件
        subprocess.run(command)

    return temp_files



def merge_video(input_file_name, output_file_name, intput_dir, temp_dir, output_dir):
    """
    将mp4文件先统一格式转换成.ts中间文件，再合并
    :param input_file_name: 输入的MP4文件的文件名（不是路径）
    :param output_file_name: 合并好的视频的文件名
    :param intput_dir: 输入的mp4文件的存放目录
    :param temp_dir: 转换好的中间文件的存放目录
    :param output_dir: 合并视频的存放目录
    :return: None
    """
    temp_files = conver_videos(input_file_name, intput_dir, temp_dir)       #将需要合并的mp4文件先转换成ts文件，再合并（直接用mp4合并会出错，用ts合并效果最好），输出的是转换好的ts文件列表

    temp_str = '|'.join(temp_files)      #需要合并的ts文件流

    output_file = os.path.join(output_dir, output_file_name)
    command = [
        'ffmpeg',
        '-i', f'concat:{temp_str}',
        '-acodec', 'copy',
        '-vcodec', 'copy',
        '-absf', 'aac_adtstoasc',
        output_file
    ]

    subprocess.run(command)

    #删除合并过程中产生的中间文件
    for ts_file in temp_files:
         os.remove(ts_file)

'''------------------------------------------视频合并代码------------------------------------------'''





if __name__ == '__main__':
    #---视频切分示例---
    # split_video(r'C:\Users\Sola的颜色\Desktop\example.mp4', r'C:\Users\Sola的颜色\Desktop\segment_videos', 20)


    #---视频合并示例---
    #输入视频的目录（需要合并的视频的目录）
    intput_dir = r"C:\Users\Sola的颜色\Desktop\segment_videos"

    #合并视频的输出目录
    output_dir = r"C:\Users\Sola的颜色\Desktop\merge_output"
    os.makedirs(output_dir, exist_ok=True)

    #合并视频过程中生成的中间文件的存放目录
    temp_dir = r"C:\Users\Sola的颜色\Desktop\temp_output"
    os.makedirs(temp_dir, exist_ok=True)

    merge_video(['segment_0.mp4', 'segment_1.mp4', 'segment_2.mp4', 'segment_3.mp4'], 'merged.mp4', intput_dir, temp_dir, output_dir)

    #测试Merge
    print("hello!")



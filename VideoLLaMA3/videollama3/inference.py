import os
import json
from glob import glob
import sys
sys.path.append('./')
from videollama3 import disable_torch_init, model_init, mm_infer
from videollama3.mm_utils import load_video

def get_video_name(json_file):
    if json_file.startswith("test_video_"):
        return json_file.replace("_qa.json", ".mp4").replace("test_video_", "test_")
    elif json_file.startswith("train_video_"):
        return json_file.replace("_qa.json", ".mp4").replace("train_video_", "train_")
    elif json_file.startswith("WebUOT"):
        return json_file.replace("_qa.json", ".mp4")
    else:
        raise ValueError(f"Unrecognized JSON file naming pattern: {json_file}")


def process_video(model, processor, video_path, json_path, output_dir):
    try:
        frames, timestamps = load_video(video_path, fps=1, max_frames=180)
    except Exception as e:
        print(f"加载视频失败 {video_path}: {str(e)}")
        return

    try:
        with open(json_path, 'r') as f:
            qa_pairs = json.load(f)
    except Exception as e:
        print(f"加载JSON失败 {json_path}: {str(e)}")
        return

    results = []
    for idx, pair in enumerate(qa_pairs):
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "video", "timestamps": timestamps, "num_frames": len(frames)},
                    {"type": "text", "text": pair["question"]},
                ]
            }
        ]
        
        try:
            inputs = processor(
                images=[frames],
                text=conversation,
                merge_size=2,
                return_tensors="pt",
            )
            
            response = mm_infer(
                inputs,
                model=model,
                tokenizer=processor.tokenizer,
                do_sample=False,
                modal="video"
            )
        except Exception as e:
            print(f"处理失败 Q{idx+1} @ {video_path}: {str(e)}")
            response = "生成失败"

        results.append({
            "video": os.path.basename(video_path),
            "question_id": idx+1,
            "question": pair["question"],
            "answer": pair.get("answer", ""),
            "generated": response
        })

    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_result.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

def batch_process(model, processor, video_dir, json_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有 JSON 文件
    json_files = glob(os.path.join(json_dir, "*.json"))

    for json_path in json_files:
        json_file = os.path.basename(json_path)
        try:
            video_file = get_video_name(json_file)
        except ValueError as e:
            print(str(e))
            continue

        video_path = os.path.join(video_dir, video_file)

        if not os.path.exists(video_path):
            print(f"未找到对应的视频文件: {video_path}")
            continue
        
        output_file = os.path.join(output_dir, f"{os.path.splitext(video_file)[0]}_result.json")
        if os.path.exists(output_file):
            print(f"已完成，跳过: {output_file}")
            continue    
            
        print(f"正在处理: {video_path}")
        process_video(model, processor, video_path, json_path, output_dir)


def main():
    disable_torch_init()
    model_path = "/home/disk/VideoLLaMA3/work_dirs/videollama3_qwen2.5_7b/stage_4-AAAI"
    model, processor = model_init(model_path)
    
    # 配置路径
    video_directory = "/home/disk/underwater-dataset/test/Test-video"     # 视频文件夹
    json_directory = "/home/disk/underwater-dataset/final-data/test"       # JSON文件夹 
    output_directory = "/home/disk/eval/AAAI/videollama-8b"    # 输出目录
    
    batch_process(model, processor, video_directory, json_directory, output_directory)

if __name__ == "__main__":
    main()
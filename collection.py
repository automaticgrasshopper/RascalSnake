import os
import glob

def collect_python_code():
    # 获取当前脚本的文件名（排除自己）
    current_script = os.path.basename(__file__)
    
    # 输出文件名
    output_file = "combined_code.txt"
    
    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 处理当前目录的Python文件
        py_files = glob.glob("*.py")
        
        for py_file in py_files:
            # 排除当前脚本文件
            if py_file == current_script:
                continue
                
            try:
                # 写入文件名作为分隔标记
                outfile.write(f"\n{'='*60}\n")
                outfile.write(f"File: {py_file}\n")
                outfile.write(f"{'='*60}\n\n")
                
                # 读取并写入文件内容
                with open(py_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write("\n\n")
                    
                print(f"已处理: {py_file}")
                
            except Exception as e:
                print(f"处理文件 {py_file} 时出错: {e}")
        
        # 处理scenes文件夹中的Python文件
        scenes_dir = "scenes"
        if os.path.exists(scenes_dir) and os.path.isdir(scenes_dir):
            scenes_py_files = glob.glob(os.path.join(scenes_dir, "*.py"))
            
            for py_file in scenes_py_files:
                try:
                    # 写入文件名作为分隔标记
                    outfile.write(f"\n{'='*60}\n")
                    outfile.write(f"File: {py_file}\n")
                    outfile.write(f"{'='*60}\n\n")
                    
                    # 读取并写入文件内容
                    with open(py_file, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n\n")
                        
                    print(f"已处理: {py_file}")
                    
                except Exception as e:
                    print(f"处理文件 {py_file} 时出错: {e}")
        else:
            print(f"未找到 {scenes_dir} 文件夹")
    
    print(f"\n所有代码已保存到: {output_file}")

if __name__ == "__main__":
    collect_python_code()
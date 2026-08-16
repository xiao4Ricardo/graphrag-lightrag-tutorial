import os
import pandas as pd

def convert_parquet_to_csv(output_dir: str = "./output", save_dir: str = "./csv_output"):
    """
    将 Microsoft GraphRAG 运行生成的 Parquet 图谱表数据批量导出转换为 CSV 格式。
    """
    if not os.path.exists(output_dir):
        print(f"指定输出目录不存在: {output_dir}")
        return

    os.makedirs(save_dir, exist_ok=True)
    
    tables = [
        "documents",
        "text_units",
        "entities",
        "relationships",
        "communities",
        "community_reports"
    ]

    for table in tables:
        parquet_file = os.path.join(output_dir, f"{table}.parquet")
        csv_file = os.path.join(save_dir, f"{table}.csv")
        
        if os.path.exists(parquet_file):
            df = pd.read_parquet(parquet_file)
            df.to_csv(csv_file, index=True)
            print(f"已导出 [{table}]: {csv_file} ({len(df)} 行)")
        else:
            print(f"未找到表文件: {parquet_file}")

if __name__ == "__main__":
    convert_parquet_to_csv()

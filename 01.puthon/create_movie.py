"""YouTube用の動画を作成するモジュール。

1枚の静止画と音楽ファイルから動画を生成する。
"""

import argparse
from pathlib import Path

from moviepy import AudioFileClip, ImageClip, concatenate_audioclips


def create_movie(
    image_path: Path,
    audio_path: Path,
    output_path: Path,
    loop_count: int = 5,
) -> None:
    """静止画と音楽から動画を作成する。

    Args:
        image_path: 画像ファイルのパス（.pngファイル）
        audio_path: 音楽ファイルのパス（.wavファイル）
        output_path: 出力動画のパス
        loop_count: 音楽のループ回数（デフォルト: 5）
    """
    # 音楽ファイルを読み込み
    audio_clip = AudioFileClip(str(audio_path))

    # 音楽を指定回数ループ
    looped_audio = concatenate_audioclips([audio_clip] * loop_count)

    # 画像クリップを作成（音楽の長さに合わせる）
    image_clip = ImageClip(str(image_path), duration=looped_audio.duration)

    # 音楽を動画に設定
    video_clip = image_clip.with_audio(looped_audio)

    # 動画を出力
    video_clip.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
    )

    # リソースを解放
    video_clip.close()
    looped_audio.close()
    audio_clip.close()


def main() -> None:
    """コマンドライン引数を解析して動画を作成する。"""
    parser = argparse.ArgumentParser(
        description="静止画と音楽からYouTube用動画を作成する"
    )
    parser.add_argument(
        "image_path",
        type=Path,
        help="画像ファイルのパス（.pngファイル）",
    )
    parser.add_argument(
        "audio_path",
        type=Path,
        help="音楽ファイルのパス（.wavファイル）",
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="出力動画のパス",
    )
    parser.add_argument(
        "--loop-count",
        type=int,
        default=5,
        help="音楽のループ回数（デフォルト: 5）",
    )

    args = parser.parse_args()

    create_movie(
        image_path=args.image_path,
        audio_path=args.audio_path,
        output_path=args.output_path,
        loop_count=args.loop_count,
    )


if __name__ == "__main__":
    main()

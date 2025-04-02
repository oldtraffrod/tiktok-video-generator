#!/bin/bash

# TikTok動画生成ツール起動スクリプト

# 必要なディレクトリが存在することを確認
mkdir -p media
mkdir -p output
mkdir -p audio

# アプリケーションを起動
echo "TikTok動画生成ツールを起動しています..."
streamlit run app.py

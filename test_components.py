import os
import shutil
import time
import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from media_search import MediaSearch
from video_generator import VideoGenerator

class TestMediaSearch(unittest.TestCase):
    """メディア検索機能のテスト"""
    
    def setUp(self):
        self.media_search = MediaSearch()
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_media")
        os.makedirs(self.test_dir, exist_ok=True)
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('media_search.requests.get')
    def test_download_media(self, mock_get):
        """メディアダウンロード機能のテスト"""
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'test_content']
        mock_get.return_value = mock_response
        
        # テスト実行
        save_path = os.path.join(self.test_dir, "test_image.jpg")
        result = self.media_search.download_media("http://example.com/image.jpg", save_path)
        
        # 検証
        self.assertTrue(result)
        self.assertTrue(os.path.exists(save_path))
        mock_get.assert_called_once_with("http://example.com/image.jpg", stream=True)
    
    @patch('media_search.PixabayImage')
    def test_search_pixabay_images(self, mock_pixabay):
        """Pixabay画像検索のテスト"""
        # モックの設定
        mock_client = MagicMock()
        mock_client.search.return_value = {
            'hits': [
                {
                    'id': '123',
                    'previewURL': 'http://example.com/preview.jpg',
                    'webformatURL': 'http://example.com/medium.jpg',
                    'largeImageURL': 'http://example.com/large.jpg',
                    'pageURL': 'http://example.com/page',
                    'webformatWidth': 800,
                    'webformatHeight': 600,
                    'tags': 'test, image'
                }
            ]
        }
        mock_pixabay.return_value = mock_client
        self.media_search.pixabay_client = mock_client
        
        # テスト実行
        results = self.media_search.search_pixabay_images("test", 1)
        
        # 検証
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], '123')
        self.assertEqual(results[0]['source'], 'Pixabay')


class TestVideoGenerator(unittest.TestCase):
    """動画生成機能のテスト"""
    
    def setUp(self):
        self.test_output_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(self.test_output_dir, exist_ok=True)
        self.video_generator = VideoGenerator(output_dir=self.test_output_dir)
    
    def tearDown(self):
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
    
    @patch('video_generator.TextClip')
    def test_create_text_clip(self, mock_text_clip):
        """テキストクリップ作成のテスト"""
        # モックの設定
        mock_clip = MagicMock()
        mock_clip.w = 500
        mock_clip.h = 100
        mock_clip.set_position.return_value = mock_clip
        mock_clip.set_duration.return_value = mock_clip
        mock_clip.fx.return_value = mock_clip
        mock_text_clip.return_value = mock_clip
        
        # テスト実行
        result = self.video_generator.create_text_clip("テストテキスト", 3, 'center')
        
        # 検証
        mock_text_clip.assert_called_once()
        self.assertEqual(mock_clip.set_duration.call_count, 1)
        self.assertEqual(mock_clip.fx.call_count, 2)  # fadein, fadeout
    
    @patch('video_generator.ImageClip')
    def test_create_image_clip(self, mock_image_clip):
        """画像クリップ作成のテスト"""
        # モックの設定
        mock_clip = MagicMock()
        mock_clip.w = 1080
        mock_clip.h = 1920
        mock_clip.resize.return_value = mock_clip
        mock_clip.crop.return_value = mock_clip
        mock_clip.set_duration.return_value = mock_clip
        mock_clip.fx.return_value = mock_clip
        mock_image_clip.return_value = mock_clip
        
        # テスト実行
        result = self.video_generator.create_image_clip("test_image.jpg", 3, False)
        
        # 検証
        mock_image_clip.assert_called_once_with("test_image.jpg")
        self.assertEqual(mock_clip.set_duration.call_count, 1)
        self.assertEqual(mock_clip.fx.call_count, 2)  # fadein, fadeout


if __name__ == '__main__':
    unittest.main()

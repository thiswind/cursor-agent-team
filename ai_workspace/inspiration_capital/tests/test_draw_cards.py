"""
Test cases for draw_cards.py
Run: python -m pytest tests/test_draw_cards.py -v
"""
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

class TestDrawCards:
    """Tests for draw_cards.py"""
    
    def setup_method(self):
        """Create temp directory with sample cards"""
        self.temp_dir = tempfile.mkdtemp()
        self.cards_dir = os.path.join(self.temp_dir, 'cards')
        os.makedirs(self.cards_dir)
        
        # Create sample cards
        for i in range(5):
            card_path = os.path.join(self.cards_dir, f'2026020{i}_120000_001.md')
            with open(card_path, 'w', encoding='utf-8') as f:
                f.write(f"""# 2026020{i}_120000_001

**时间**: 2026-02-0{i} 12:00:00
**来源**: test
**触发**: test trigger {i}

---

This is test content {i}

---

**为什么有意思**: reason {i}
""")
    
    def teardown_method(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)
    
    def test_draws_specified_number_of_cards(self):
        """Should draw exactly N cards when N cards exist"""
        from draw_cards import draw_cards
        result = draw_cards(cards_dir=self.cards_dir, count=3)
        assert result['count'] == 3
        assert len(result['cards']) == 3
    
    def test_draws_all_if_fewer_than_requested(self):
        """Should draw all cards if fewer than requested exist"""
        from draw_cards import draw_cards
        result = draw_cards(cards_dir=self.cards_dir, count=10)
        assert result['count'] == 5  # Only 5 cards exist
        assert len(result['cards']) == 5
    
    def test_returns_empty_for_empty_directory(self):
        """Should return empty result for empty cards directory"""
        from draw_cards import draw_cards
        empty_dir = os.path.join(self.temp_dir, 'empty')
        os.makedirs(empty_dir)
        result = draw_cards(cards_dir=empty_dir, count=3)
        assert result['count'] == 0
        assert len(result['cards']) == 0
    
    def test_output_contains_required_fields(self):
        """Each card in output should have required fields"""
        from draw_cards import draw_cards
        result = draw_cards(cards_dir=self.cards_dir, count=1)
        card = result['cards'][0]
        assert 'filename' in card
        assert 'time' in card
        assert 'source' in card
        assert 'trigger' in card
        assert 'content' in card
    
    def test_format_output_produces_structured_text(self):
        """format_output should produce human-readable structured text"""
        from draw_cards import draw_cards, format_output
        result = draw_cards(cards_dir=self.cards_dir, count=2)
        text = format_output(result)
        assert '=== 随机抽取结果 ===' in text
        assert '--- 卡片 1/' in text
        assert '--- 卡片 2/' in text
        assert '=== 抽取结束 ===' in text

"""
Test cases for create_card.py
Run: python -m pytest tests/test_create_card.py -v
"""
import os
import sys
import tempfile
import shutil
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

class TestCreateCard:
    """Tests for create_card.py"""
    
    def setup_method(self):
        """Create temp directory for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.cards_dir = os.path.join(self.temp_dir, 'cards')
        os.makedirs(self.cards_dir)
    
    def teardown_method(self):
        """Clean up temp directory"""
        shutil.rmtree(self.temp_dir)
    
    def test_creates_file_with_timestamp_filename(self):
        """Card filename should contain timestamp in YYYYMMDD_HHMMSS format"""
        from create_card import create_card
        filepath = create_card(
            cards_dir=self.cards_dir,
            source="test",
            trigger="test trigger"
        )
        filename = os.path.basename(filepath)
        # Should match pattern: YYYYMMDD_HHMMSS_NNN.md
        assert filename.endswith('.md')
        parts = filename.replace('.md', '').split('_')
        assert len(parts) == 3
        assert len(parts[0]) == 8  # YYYYMMDD
        assert len(parts[1]) == 6  # HHMMSS
        assert parts[2].isdigit()  # sequence number
    
    def test_creates_file_with_required_fields(self):
        """Card should contain all required fields"""
        from create_card import create_card
        filepath = create_card(
            cards_dir=self.cards_dir,
            source="Moltbook",
            trigger="看到有趣的讨论"
        )
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert '**时间**:' in content
        assert '**来源**: Moltbook' in content
        assert '**触发**: 看到有趣的讨论' in content
        assert '[内容待填写]' in content
        assert '**为什么有意思**:' in content
    
    def test_increments_sequence_number(self):
        """Multiple cards in same second should have different sequence numbers"""
        from create_card import create_card
        filepath1 = create_card(cards_dir=self.cards_dir, source="test", trigger="t1")
        filepath2 = create_card(cards_dir=self.cards_dir, source="test", trigger="t2")
        
        # Should be different files
        assert filepath1 != filepath2
        assert os.path.exists(filepath1)
        assert os.path.exists(filepath2)
    
    def test_returns_absolute_path(self):
        """Should return absolute path to created file"""
        from create_card import create_card
        filepath = create_card(cards_dir=self.cards_dir, source="test", trigger="test")
        assert os.path.isabs(filepath)
        assert os.path.exists(filepath)

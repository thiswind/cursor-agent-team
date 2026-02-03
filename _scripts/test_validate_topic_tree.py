#!/usr/bin/env python3
"""
TDD Tests for Topic Tree Auto-Compress Feature

Run with: python -m pytest test_validate_topic_tree.py -v
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from validate_topic_tree import (
    extract_topic_ids,
    parse_topic_metadata,
    should_archive_topic,
    compress_topic_to_index,
    generate_archive_content,
    auto_compress_topic_tree,
    ARCHIVE_COOLDOWN_DAYS,
)


class TestExtractTopicIds:
    """Test ID extraction (existing functionality)"""
    
    def test_bracket_format(self):
        content = "### [A] Topic Name\n### [B] Another Topic"
        ids = extract_topic_ids(content)
        assert ids == {"A", "B"}
    
    def test_table_format(self):
        content = "| A | Topic Name | completed |\n| B | Another | completed |"
        ids = extract_topic_ids(content)
        assert ids == {"A", "B"}
    
    def test_sub_topic_ids(self):
        """New: support A.1 format"""
        content = "### [A] Topic\n### [A.1] Sub Topic\n### [B] Another"
        ids = extract_topic_ids(content)
        assert ids == {"A", "A.1", "B"}


class TestParseTopicMetadata:
    """Test parsing topic metadata from topic block"""
    
    def test_parse_completed_topic(self):
        content = """### [A] Topic Name
- Status: completed
- Created: 2026-02-01 10:00
- Last Active: 2026-02-01 12:00
- Keywords: test, example

#### Discussion Points
1. Point one
2. Point two
"""
        metadata = parse_topic_metadata(content, "A")
        assert metadata["id"] == "A"
        assert metadata["title"] == "Topic Name"
        assert metadata["status"] == "completed"
        assert metadata["last_active"] == "2026-02-01 12:00"
    
    def test_parse_in_progress_topic(self):
        content = """### [B] Active Topic
- Status: in_progress
- Created: 2026-02-03 10:00
"""
        metadata = parse_topic_metadata(content, "B")
        assert metadata["status"] == "in_progress"


class TestShouldArchiveTopic:
    """Test archive condition checking"""
    
    def test_completed_old_topic_should_archive(self):
        """completed + older than cooldown days = should archive"""
        old_date = (datetime.now() - timedelta(days=ARCHIVE_COOLDOWN_DAYS + 1)).strftime("%Y-%m-%d %H:%M")
        metadata = {
            "status": "completed",
            "last_active": old_date
        }
        assert should_archive_topic(metadata) is True
    
    def test_completed_recent_topic_should_not_archive(self):
        """completed but within cooldown = should NOT archive"""
        recent_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        metadata = {
            "status": "completed",
            "last_active": recent_date
        }
        assert should_archive_topic(metadata) is False
    
    def test_in_progress_topic_should_not_archive(self):
        """in_progress = should NEVER archive"""
        old_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
        metadata = {
            "status": "in_progress",
            "last_active": old_date
        }
        assert should_archive_topic(metadata) is False


class TestCompressTopicToIndex:
    """Test compressing full topic to index row"""
    
    def test_generate_index_row(self):
        metadata = {
            "id": "A",
            "title": "Project Understanding",
            "status": "completed",
            "last_active": "2026-02-01 12:00"
        }
        row = compress_topic_to_index(metadata)
        assert "| A |" in row
        assert "Project Understanding" in row
        assert "completed" in row


class TestGenerateArchiveContent:
    """Test generating archive file content"""
    
    def test_archive_file_format(self):
        topic_block = """### [A] Project Understanding
- Status: completed
- Created: 2026-02-01 10:00
- Last Active: 2026-02-01 12:00

#### Discussion Points
1. First point
2. Second point
"""
        metadata = {
            "id": "A",
            "title": "Project Understanding",
            "status": "completed"
        }
        archive_content = generate_archive_content(topic_block, metadata)
        assert "# Topic [A] - Project Understanding" in archive_content
        assert "Archived:" in archive_content
        assert "Discussion Points" in archive_content


class TestAutoCompressTopicTree:
    """Integration tests for auto-compress feature"""
    
    def test_compress_old_completed_topics(self):
        """Old completed topics should be compressed to index"""
        old_date = (datetime.now() - timedelta(days=ARCHIVE_COOLDOWN_DAYS + 1)).strftime("%Y-%m-%d %H:%M")
        
        input_content = f"""# Discussion Topics Tree

> Last Updated: 2026-02-03 19:00:00

## Active Topic

[B] Active Topic

## Topic Tree

### [A] Old Completed Topic
- Status: completed
- Created: 2026-02-01 10:00
- Last Active: {old_date}

#### Discussion Points
1. Some discussion

---

### [B] Active Topic
- Status: in_progress
- Created: 2026-02-03 10:00

#### Discussion Points
1. Current work
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_dir = Path(tmpdir) / "topic_archives"
            compressed, archives = auto_compress_topic_tree(input_content, archive_dir)
            
            # Index should contain A
            assert "| A |" in compressed
            # Full [A] topic should NOT be in main file
            assert "### [A] Old Completed Topic" not in compressed
            # [B] should remain full
            assert "### [B] Active Topic" in compressed
            # Archive file should be created
            assert len(archives) == 1
            assert "A" in archives
    
    def test_keep_recent_completed_topics(self):
        """Recent completed topics should NOT be compressed"""
        recent_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        input_content = f"""# Discussion Topics Tree

> Last Updated: 2026-02-03 19:00:00

## Topic Tree

### [A] Recent Completed Topic
- Status: completed
- Last Active: {recent_date}

#### Discussion Points
1. Some discussion
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_dir = Path(tmpdir) / "topic_archives"
            compressed, archives = auto_compress_topic_tree(input_content, archive_dir)
            
            # Should remain full (not compressed)
            assert "### [A] Recent Completed Topic" in compressed
            assert len(archives) == 0
    
    def test_r1_validation_still_passes(self):
        """After compression, R1 validation should still pass"""
        from validate_topic_tree import check_r1_id_preservation
        
        old_content = """### [A] Topic A
### [B] Topic B
"""
        new_content = """## Topic Index
| A | Topic A | completed |

### [B] Topic B
"""
        errors = check_r1_id_preservation(old_content, new_content)
        assert len(errors) == 0  # A is in index, B is full


class TestSubTopicIdExtraction:
    """Test that sub-topic IDs (A.1 format) are properly handled"""
    
    def test_extract_subtopic_ids(self):
        content = """### [D] Parent Topic
### [D.1] Child Topic
"""
        ids = extract_topic_ids(content)
        assert "D" in ids
        assert "D.1" in ids

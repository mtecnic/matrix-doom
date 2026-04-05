"""Tests for utils module."""

import json
import os
import tempfile
import pytest

from utils import Vec2, clamp, lerp
from utils.file_io import (
    read_text_file,
    read_json_file,
    write_text_file,
    write_json_file,
    ensure_directory,
    file_exists,
    get_file_size,
)


class TestVec2:
    """Tests for Vec2 class."""

    def test_creation(self):
        """Test Vec2 creation."""
        v = Vec2(3.0, 4.0)
        assert v.x == 3.0
        assert v.y == 4.0

    def test_addition(self):
        """Test Vec2 addition."""
        v1 = Vec2(1.0, 2.0)
        v2 = Vec2(3.0, 4.0)
        result = v1 + v2
        assert result.x == 4.0
        assert result.y == 6.0

    def test_subtraction(self):
        """Test Vec2 subtraction."""
        v1 = Vec2(5.0, 7.0)
        v2 = Vec2(2.0, 3.0)
        result = v1 - v2
        assert result.x == 3.0
        assert result.y == 4.0

    def test_scalar_multiplication(self):
        """Test Vec2 scalar multiplication."""
        v = Vec2(2.0, 3.0)
        result = v * 2.0
        assert result.x == 4.0
        assert result.y == 6.0

    def test_scalar_division(self):
        """Test Vec2 scalar division."""
        v = Vec2(4.0, 6.0)
        result = v / 2.0
        assert result.x == 2.0
        assert result.y == 3.0

    def test_dot_product(self):
        """Test Vec2 dot product."""
        v1 = Vec2(1.0, 2.0)
        v2 = Vec2(3.0, 4.0)
        result = v1.dot(v2)
        assert result == 11.0  # 1*3 + 2*4

    def test_length(self):
        """Test Vec2 length (magnitude)."""
        v = Vec2(3.0, 4.0)
        assert v.length() == 5.0

    def test_distance(self):
        """Test Vec2 distance."""
        v1 = Vec2(0.0, 0.0)
        v2 = Vec2(3.0, 4.0)
        assert v1.distance(v2) == 5.0

    def test_normalize(self):
        """Test Vec2 normalization."""
        v = Vec2(3.0, 4.0)
        normalized = v.normalize()
        assert normalized.x == 0.6
        assert normalized.y == 0.8

    def test_normalize_zero_vector(self):
        """Test Vec2 normalization of zero vector."""
        v = Vec2(0.0, 0.0)
        normalized = v.normalize()
        assert normalized.x == 0.0
        assert normalized.y == 0.0

    def test_to_tuple(self):
        """Test Vec2 to_tuple method."""
        v = Vec2(1.5, 2.5)
        result = v.to_tuple()
        assert result == (1.5, 2.5)

    def test_immutability(self):
        """Test that Vec2 is immutable."""
        v = Vec2(1.0, 2.0)
        with pytest.raises(AttributeError):
            v.x = 5.0


class TestClamp:
    """Tests for clamp function."""

    def test_clamp_within_range(self):
        """Test clamping a value within range."""
        assert clamp(5.0, 0.0, 10.0) == 5.0

    def test_clamp_below_range(self):
        """Test clamping a value below range."""
        assert clamp(-5.0, 0.0, 10.0) == 0.0

    def test_clamp_above_range(self):
        """Test clamping a value above range."""
        assert clamp(15.0, 0.0, 10.0) == 10.0

    def test_clamp_edge_cases(self):
        """Test clamp edge cases."""
        assert clamp(0.0, 0.0, 10.0) == 0.0
        assert clamp(10.0, 0.0, 10.0) == 10.0


class TestLerp:
    """Tests for lerp function."""

    def test_lerp_at_t0(self):
        """Test lerp at t=0."""
        assert lerp(0.0, 10.0, 0.0) == 0.0

    def test_lerp_at_t1(self):
        """Test lerp at t=1."""
        assert lerp(0.0, 10.0, 1.0) == 10.0

    def test_lerp_midpoint(self):
        """Test lerp at midpoint."""
        assert lerp(0.0, 10.0, 0.5) == 5.0

    def test_lerp_with_negative_values(self):
        """Test lerp with negative values."""
        assert lerp(-5.0, 5.0, 0.5) == 0.0

    def test_lerp_clamps_t(self):
        """Test that lerp clamps t to [0, 1]."""
        assert lerp(0.0, 10.0, -1.0) == 0.0
        assert lerp(0.0, 10.0, 2.0) == 10.0


class TestFileIO:
    """Tests for file I/O utilities."""

    def setup_method(self):
        """Set up temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_read_text_file_exists(self):
        """Test reading an existing text file."""
        filepath = os.path.join(self.temp_dir, "test.txt")
        with open(filepath, "w") as f:
            f.write("Hello, World!\n")

        result = read_text_file(filepath)
        assert result == "Hello, World!"

    def test_read_text_file_not_exists(self):
        """Test reading a non-existent file returns default."""
        result = read_text_file("/nonexistent/path/file.txt")
        assert result == ""

    def test_read_text_file_custom_default(self):
        """Test reading a non-existent file with custom default."""
        result = read_text_file("/nonexistent/path/file.txt", default="default")
        assert result == "default"

    def test_read_json_file_valid(self):
        """Test reading a valid JSON file."""
        filepath = os.path.join(self.temp_dir, "test.json")
        data = {"key": "value", "number": 42}
        with open(filepath, "w") as f:
            json.dump(data, f)

        result = read_json_file(filepath)
        assert result == data

    def test_read_json_file_not_exists(self):
        """Test reading a non-existent JSON file."""
        result = read_json_file("/nonexistent/path/file.json")
        assert result == {}

    def test_read_json_file_custom_default(self):
        """Test reading a non-existent JSON file with custom default."""
        result = read_json_file("/nonexistent/path/file.json", default={})
        assert result == {}

    def test_read_json_file_invalid(self):
        """Test reading an invalid JSON file."""
        filepath = os.path.join(self.temp_dir, "invalid.json")
        with open(filepath, "w") as f:
            f.write("{invalid json}")

        result = read_json_file(filepath)
        assert result == {}

    def test_write_text_file_success(self):
        """Test writing text to a file."""
        filepath = os.path.join(self.temp_dir, "output.txt")
        result = write_text_file(filepath, "Hello, World!")

        assert result is True
        assert os.path.exists(filepath)
        with open(filepath, "r") as f:
            assert f.read() == "Hello, World!"

    def test_write_text_file_creates_dirs(self):
        """Test that write_text_file creates directories."""
        filepath = os.path.join(self.temp_dir, "subdir", "output.txt")
        result = write_text_file(filepath, "Hello, World!")

        assert result is True
        assert os.path.exists(filepath)

    def test_write_text_file_no_mkdir(self):
        """Test write_text_file with mkdir=False."""
        filepath = os.path.join(self.temp_dir, "output.txt")
        result = write_text_file(filepath, "Hello, World!", mkdir=False)

        assert result is True
        assert os.path.exists(filepath)

    def test_write_json_file_success(self):
        """Test writing JSON to a file."""
        filepath = os.path.join(self.temp_dir, "output.json")
        data = {"key": "value", "number": 42}
        result = write_json_file(filepath, data)

        assert result is True
        assert os.path.exists(filepath)
        with open(filepath, "r") as f:
            loaded = json.load(f)
            assert loaded == data

    def test_write_json_file_creates_dirs(self):
        """Test that write_json_file creates directories."""
        filepath = os.path.join(self.temp_dir, "subdir", "output.json")
        result = write_json_file(filepath, {"key": "value"})

        assert result is True
        assert os.path.exists(filepath)

    def test_write_json_file_invalid_data(self):
        """Test writing invalid data returns False."""
        filepath = os.path.join(self.temp_dir, "output.json")
        # lambda is not JSON serializable
        result = write_json_file(filepath, lambda: None)

        assert result is False

    def test_ensure_directory_exists(self):
        """Test ensuring a directory exists."""
        dirpath = os.path.join(self.temp_dir, "newdir")
        result = ensure_directory(dirpath)

        assert result is True
        assert os.path.isdir(dirpath)

    def test_ensure_directory_already_exists(self):
        """Test ensuring an existing directory."""
        dirpath = os.path.join(self.temp_dir, "existing")
        os.makedirs(dirpath, exist_ok=True)
        result = ensure_directory(dirpath)

        assert result is True

    def test_file_exists_true(self):
        """Test file_exists with existing file."""
        filepath = os.path.join(self.temp_dir, "test.txt")
        with open(filepath, "w") as f:
            f.write("test")

        assert file_exists(filepath) is True

    def test_file_exists_false(self):
        """Test file_exists with non-existing file."""
        assert file_exists("/nonexistent/path/file.txt") is False

    def test_get_file_size(self):
        """Test getting file size."""
        filepath = os.path.join(self.temp_dir, "test.txt")
        with open(filepath, "w") as f:
            f.write("Hello")

        size = get_file_size(filepath)
        assert size == 5

    def test_get_file_size_nonexistent(self):
        """Test getting size of non-existent file."""
        size = get_file_size("/nonexistent/path/file.txt")
        assert size == 0

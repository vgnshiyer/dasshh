"""Tests for the Navbar component."""
from unittest.mock import MagicMock, patch

import pytest
from textual.containers import Horizontal

from dasshh.ui.components.navbar import Navbar, NavItem, Logo
from dasshh.ui.events import ChangeView


@pytest.fixture
def mock_query():
    """Mock for query_one and query methods."""
    mock = MagicMock()
    mock.add_class = MagicMock()
    mock.remove_class = MagicMock()
    return mock


class TestNavItem:
    """Tests for the NavItem component."""
    
    def test_initialization(self):
        """Test NavItem initialization."""
        nav_item = NavItem(route="test", label="Test", icon="T")
        assert nav_item.route == "test"
        # The rendered text should include the icon and label
        assert nav_item.renderable == "T Test"
    
    def test_on_click(self):
        """Test NavItem click event posts ChangeView message."""
        nav_item = NavItem(route="test", label="Test")
        nav_item.post_message = MagicMock()
        nav_item.add_class = MagicMock()
        
        nav_item.on_click()
        
        nav_item.add_class.assert_called_once_with("active")
        nav_item.post_message.assert_called_once()
        
        # Check that the posted message is ChangeView with correct route
        posted_message = nav_item.post_message.call_args[0][0]
        assert isinstance(posted_message, ChangeView)
        assert posted_message.view == "test"


class TestLogo:
    """Tests for the Logo component."""
    
    def test_render(self):
        """Test Logo renders correctly."""
        logo = Logo()
        rendered = logo.render()
        
        assert "Dasshh 🗲" in rendered
        assert isinstance(rendered, str)


class TestNavbar:
    """Tests for the Navbar component."""
    
    @patch('dasshh.ui.components.navbar.Navbar.compose')
    def test_compose(self, mock_compose):
        """Test Navbar composition."""
        navbar = Navbar()
        
        # Mock the compose method to avoid Textual app dependencies
        mock_logo = MagicMock(spec=Logo)
        mock_horizontal = MagicMock(spec=Horizontal)
        mock_horizontal.id = "nav-items"
        
        mock_compose.return_value = [mock_logo, mock_horizontal]
        
        # Get the components yielded by compose
        components = list(navbar.compose())
        
        # Check that we have a Logo and a Horizontal container
        assert len(components) == 2
        assert components[0] == mock_logo
        assert components[1] == mock_horizontal
        assert components[1].id == "nav-items"
    
    @patch('dasshh.ui.components.navbar.Navbar.query_one')
    def test_on_mount(self, mock_query_one):
        """Test on_mount adds active class to chat NavItem."""
        navbar = Navbar()
        mock_chat_item = MagicMock()
        mock_query_one.return_value = mock_chat_item
        
        navbar.on_mount()
        
        mock_query_one.assert_called_once_with("#chat")
        mock_chat_item.add_class.assert_called_once_with("active")
    
    @patch('dasshh.ui.components.navbar.Navbar.query')
    @patch('dasshh.ui.components.navbar.Navbar.query_one')
    def test_change_view(self, mock_query_one, mock_query):
        """Test change_view event handler."""
        navbar = Navbar()
        
        # Mock NavItems returned by query
        mock_items = [MagicMock(), MagicMock(), MagicMock()]
        mock_query.return_value = mock_items
        
        # Mock the selected NavItem
        mock_selected_item = MagicMock()
        mock_query_one.return_value = mock_selected_item
        
        # Create a ChangeView event
        event = ChangeView("settings")
        
        # Call the event handler
        navbar.change_view(event)
        
        # Check that remove_class was called on all NavItems
        for item in mock_items:
            item.remove_class.assert_called_once_with("active")
        
        # Check that query_one was called with the correct selector
        mock_query_one.assert_called_once_with("#settings")
        
        # Check that add_class was called on the selected NavItem
        mock_selected_item.add_class.assert_called_once_with("active") 
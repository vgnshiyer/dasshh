"""Tests for the Action component."""
from unittest.mock import MagicMock, patch, PropertyMock

from rich.console import Group
from rich.syntax import Syntax
from rich.text import Text

from dasshh.ui.components.chat.action import Action


def test_action_initialization():
    """Test Action initialization."""
    action = Action(
        invocation_id="test_invocation",
        tool_call_id="test_tool_call",
        name="test_tool",
        args='{"param": "value"}',
        result='{"result": "success"}'
    )

    assert action.invocation_id == "test_invocation"
    assert action.tool_call_id == "test_tool_call"
    assert action.name == "test_tool"
    assert action.args == '{"param": "value"}'
    assert action.result == '{"result": "success"}'


@patch('dasshh.ui.components.chat.action.Syntax')
@patch.object(Action, 'app', new_callable=PropertyMock)
def test_action_render_with_result(mock_app_prop, mock_syntax):
    """Test rendering an action with a result."""
    mock_app = MagicMock()
    mock_app.get_css_variables.return_value = {"panel": "#123456"}
    mock_app_prop.return_value = mock_app

    mock_args_syntax = MagicMock(spec=Syntax)
    mock_result_syntax = MagicMock(spec=Syntax)
    mock_syntax.side_effect = [mock_args_syntax, mock_result_syntax]

    action = Action(
        invocation_id="test_invocation",
        tool_call_id="test_tool_call",
        name="test_tool",
        args='{"param": "value"}',
        result='{"result": "success"}'
    )

    rendered = action.render()

    assert mock_syntax.call_count == 2
    args_call, result_call = mock_syntax.call_args_list

    assert args_call[0][0] == '{"param": "value"}'
    assert args_call[0][1] == "json"
    assert args_call[1]["background_color"] == "#123456"
    assert result_call[0][0] == '{"result": "success"}'
    assert result_call[0][1] == "json"
    assert result_call[1]["background_color"] == "#123456"

    assert isinstance(rendered, Group)
    assert len(rendered.renderables) == 5

    assert isinstance(rendered.renderables[0], Text)
    assert "Using tool: test_tool" in rendered.renderables[0].plain

    assert rendered.renderables[1] == mock_args_syntax

    assert isinstance(rendered.renderables[2], Text)
    assert rendered.renderables[2].plain == ""

    assert isinstance(rendered.renderables[3], Text)
    assert "Result: test_tool" in rendered.renderables[3].plain
    assert rendered.renderables[4] == mock_result_syntax


@patch('dasshh.ui.components.chat.action.Syntax')
@patch.object(Action, 'app', new_callable=PropertyMock)
def test_action_render_without_result(mock_app_prop, mock_syntax):
    """Test rendering an action without a result."""
    mock_app = MagicMock()
    mock_app.get_css_variables.return_value = {"panel": "#123456"}
    mock_app_prop.return_value = mock_app
    mock_args_syntax = MagicMock(spec=Syntax)
    mock_syntax.return_value = mock_args_syntax

    action = Action(
        invocation_id="test_invocation",
        tool_call_id="test_tool_call",
        name="test_tool",
        args='{"param": "value"}',
        result=''
    )

    rendered = action.render()

    mock_syntax.assert_called_once_with(
        '{"param": "value"}',
        "json",
        background_color="#123456",
        word_wrap=True
    )

    assert isinstance(rendered, Group)
    assert len(rendered.renderables) == 2

    assert isinstance(rendered.renderables[0], Text)
    assert "Using tool: test_tool" in rendered.renderables[0].plain
    assert rendered.renderables[1] == mock_args_syntax

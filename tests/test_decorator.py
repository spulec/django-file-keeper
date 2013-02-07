from mock import patch
import sure

from keeper.core import use_file

@patch("keeper.core.Keeper.get_file")
def test_basic_decorator(get_file):
    get_file.return_value = ["test1", "test2"]

    @use_file('foobar.csv')
    def a_handle(the_file, *args, **options):
        lines = []
        for line in the_file:
            lines.append(line)
        return lines

    a_handle.when.called_with().should.return_value(["test1", "test2"])

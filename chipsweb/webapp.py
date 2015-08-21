import web
import StringIO
from web import form
from chips.compiler.parser import Parser
from chips.compiler.exceptions import C2CHIPError
from chips.compiler.macro_expander import expand_macros
from chips.compiler.verilog_area import generate_CHIP as generate_CHIP_area
from pygments import highlight
from pygments.lexers.hdl import VerilogLexer
from pygments.formatters import HtmlFormatter
from examples import examples


render = web.template.render('templates/')
        
urls = (
    '/', 'source_entry',
    '/main.v', 'file_download'
)
app = web.application(urls, globals())

myform = form.Form(
        form.Textarea("C"),
        form.Dropdown("Examples", examples.keys(), onclick = "return update_form()"),
)

class file_download:        
    def POST(self):
        f = myform()
        f.validates()
        try:
            code = compile(f["C"].value)
            web.header("content-type", "application/octet-stream")
            web.header("content-transfer-encoding", "binary")
            return code
        except C2CHIPError as err:
            return "Error in file: " + err.filename + " at line: " + str(err.lineno) + "\n" + err.message

class source_entry:        
    def GET(self):
        f = myform()
        f["C"].value="void main(){}"
        return render.page(f)

    def POST(self):
        f = myform()
        f.validates()
        example_selected=f["Examples"].value
        f["C"].value=examples[example_selected]
        f["Examples"].value=example_selected
        return render.page(f)

def compile(c_buffer):

    input_file = open("main.c", 'w')
    input_file.write(c_buffer)
    input_file.close()

    parser = Parser("main.c", False, False, [])
    process = parser.parse_process()
    name = process.main.name
    instructions = process.generate()
    instructions = expand_macros(instructions, parser.allocator)

    output_file = StringIO.StringIO()

    inputs, outputs = generate_CHIP_area(
            input_file,
            name,
            instructions,
            output_file,
            parser.allocator,
            False)

    return output_file.getvalue()

if __name__ == "__main__":
    app.run()

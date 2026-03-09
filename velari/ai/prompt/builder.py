import  pandas as pd
import  jinja2 as j2
import  textwrap
from    typing import Optional, Dict, Any
from    pathlib import Path
from    omegaconf import DictConfig
# package modules
from    ...core.io.partition.hydra import read_hydra

class PromptBuilder(object):
    """Build and format prompts from a YAML-backed catalog of named templates."""

    def __init__(self, uri: Optional[str] = None, key: Optional[str] = None):
        """Load the prompt catalog from a YAML file and initialise the DataFrame index.

        Args:
            uri: Path to the YAML catalog file. When None, the catalog is empty.
            key: Top-level key within the YAML file that contains the template list.
                When None, an empty dict is used as the catalog source.
        """
        self.df_catalog = pd.DataFrame(self.load_catalog(uri=uri, key=key))

    def load_catalog(self, uri: str, key: Optional[str] = None) -> DictConfig:
        """Load a named section from a Hydra YAML file and return it as a config object.

        Args:
            uri: Path to the YAML file to read.
            key: Top-level key whose value is returned. Defaults to an empty dict when
                the key is absent or None.

        Returns:
            The value stored under ``key`` in the parsed YAML, or an empty dict if the
            key is not present.
        """
        return read_hydra(filepath=uri).get(key, {})

    def get_template(self, name: str) -> str:
        """Retrieve the raw template string for a named prompt entry.

        Args:
            name: Name of the prompt entry to look up in the catalog.

        Returns:
            Raw template string associated with the given name.
        """
        template   =  self.df_catalog.query("name == @name", inplace=False).loc[0, "template"]
        return template

    def format_template(self, name: str, **kwargs) -> str:
        """Retrieve and format a named template with the provided keyword arguments.

        Args:
            name: Name of the prompt entry to look up in the catalog.
            **kwargs: Placeholder values to substitute into the template via
                ``str.format``.

        Returns:
            Formatted string with all placeholders replaced by their corresponding values.

        Examples:
            >>> builder = PromptBuilder(uri="config/prompts/catalog.yaml", key="prompts")
            >>> text = builder.format_template("summarise", topic="climate change", length=200)
        """
        template = self.get_template(name)
        return template.format(**kwargs)


class TemplateJ2(object):
    """Load and render Jinja2 prompt template files from a directory.

    Examples:
        >>> prompt_exec = TemplateJ2(template_path=exp.conf_dir.joinpath("prompts"))
        >>> template: j2.Template = prompt_exec.load_template("child.j2")
        >>> output: str = prompt_exec.render("child.j2", content={"name": "John"})
    """

    def __init__(self, template_path: Optional[str] = None, **kwargs):
        """Initialise the Jinja2 environment with common Python builtins and trim settings.

        Configures the environment to strip leading whitespace and trailing newlines,
        and exposes ``isinstance``, ``hasattr``, ``type``, and ``len`` as global
        functions within templates. No environment is created when ``template_path``
        is None.

        Args:
            template_path: Directory containing the Jinja2 template files. When None,
                only ``render_from_string`` is usable.
            **kwargs: Reserved for future extension; currently unused.
        """
        params = dict(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            undefined=j2.DebugUndefined,
        )
        if template_path is not None:
            self.template_path = Path(template_path)
            self.env = j2.Environment(loader=j2.FileSystemLoader(self.template_path), **params)
            # make some python core functionality available in template files
            self.env.globals["isinstance"] = isinstance
            self.env.globals["hasattr"]    = hasattr
            self.env.globals["type"]       = type
            self.env.globals["len"]        = len

    def load_text(self, file_path: str) -> str:
        """Load a Jinja2 template file as a raw stripped text string.

        Args:
            file_path: Relative path to the ``*.j2`` file within ``template_path``.

        Returns:
            Contents of the file with leading and trailing whitespace removed.
        """
        with open(self.template_path.joinpath(file_path), "r", encoding="utf-8") as file:
            return file.read().strip()

    def load_source(self, template_file: str) -> str:
        """Retrieve the Jinja2 template source string via the environment loader.

        Args:
            template_file: Name of the ``*.j2`` file to load from the template directory.

        Returns:
            Raw template source string with leading and trailing whitespace removed.
        """
        source, filename, uptodate = self.env.loader.get_source(self.env, template_file)
        return source.strip()

    def load_template(self, template_file: str) -> j2.Template:
        """Load and return a compiled Jinja2 Template object.

        Args:
            template_file: Name of the ``*.j2`` file to compile from the template directory.

        Returns:
            Compiled ``jinja2.Template`` ready for rendering.
        """
        template = self.env.get_template(template_file)
        return template

    @classmethod
    def render_from_string(cls, template_string: str, template_context: Dict[str, Any], **kwargs) -> str:
        """Render a Jinja2 template string directly without a file loader.

        Args:
            template_string: Raw Jinja2 template string to compile and render.
            template_context: Mapping of variable names to values available inside the template.
            **kwargs: Additional variables merged into the render context.

        Returns:
            Rendered output string with all template expressions evaluated.

        Examples:
            >>> output = TemplateJ2.render_from_string("Hello, {{ name }}!", {"name": "Ada"})
        """
        template = j2.Template(template_string)
        output = template.render(template_context, **kwargs)
        return output

    def render(self, template_file: str, content: dict, **kwargs) -> str:
        """Render a Jinja2 template file with the given content dictionary.

        Args:
            template_file: Name of the ``*.j2`` file in the template directory to render.
            content: Mapping of variable names to values passed into the template context.
            **kwargs: Additional variables merged into the render context.

        Returns:
            Rendered and dedented string with trailing whitespace removed.

        Examples:
            >>> prompt_exec = TemplateJ2(template_path="config/prompts")
            >>> output = prompt_exec.render("child.j2", content={"name": "John", "age": 30})
        """
        template = self.env.get_template(template_file)
        output = template.render(content, **kwargs)
        return textwrap.dedent(output.rstrip())

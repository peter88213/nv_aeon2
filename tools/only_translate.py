"""Create a German translation."""
import build

pb = build.PluginBuilder(build.VERSION)
pb.build_py_module()
pb.build_translation()
pb.clean_up()


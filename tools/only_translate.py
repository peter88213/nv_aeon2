"""Create a German translation."""
import build

pb = build.PluginBuilder(build.VERSION)
pb.build_script()
pb.build_translation()
pb.clean_up()


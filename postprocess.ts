const apt_install = Deno.run({
  cmd: ['sudo', 'apt-get', 'install', "libegl1", "libopus0", "libwoff1", "libharfbuzz-icu0", "gstreamer1.0-plugins-base", "libgstreamer-gl1.0-0", "gstreamer1.0-plugins-bad", "libopenjp2-7", "libwebpdemux2", "libenchant1c2a", "libhyphen0", "libgles2", "gstreamer1.0-libav", "libevdev-dev"],
});

await apt_install.status();


// install requirements with pip
const pip_install = Deno.run({
  cmd: ['python', '-m', 'pip', 'install', '-r', 'requirements.txt'],
});

await pip_install.status();

const playwright_install = Deno.run({
  cmd: ['python', '-m', 'playwright', 'install'],
});

await playwright_install.status();

const playwright_configure = Deno.run({
  cmd: ['sudo', 'npx', 'playwright', 'install-deps'],
});

await playwright_configure.status();


// Forwards the execution to the python script
const py_run = Deno.run({
  cmd: ['python', './postprocessing.py'].concat(Deno.args),
});

await py_run.status();

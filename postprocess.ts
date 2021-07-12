// install requirements with pip
const pip_install = Deno.run({
  cmd: ['python', '-m', 'pip', 'install', '-r', 'requirements.txt'],
});

await pip_install.status();

const playwright_install = Deno.run({
  cmd: ['python', '-m', 'playwright', 'install'],
});

await playwright_install.status();

// Forwards the execution to the python script
const py_run = Deno.run({
  cmd: ['python', './postprocessing.py'].concat(Deno.args),
});

await py_run.status();

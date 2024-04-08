import click, os, sys
from pydotenvs.main import load_env_cli, load_env, load_env_object, transfer_new_env, clear_env
from pydotenvs.version import __version__


@click.command('pydotenvs')
@click.option('-f', '--envpath', required=1, default=os.path.join(os.getcwd(), '.env'), type=click.Path(exists=True), help='Location of .env file, defaults to .env in current working directory')
@click.option('-n', '--newpath', type=click.Path(exists=True), help='Location of new .env file that you would like to transfer old env file variables to')
@click.option('-t', '--transfer', default=False, type=click.BOOL, help='This must be true if you would like to transfer. --newpath is required as well.')
@click.option('-p', '--preserve', default=True, type=click.BOOL, help='True or False whether or not to preserve existing envs during transfer')
@click.option('-c', '--command', type=click.STRING, help='Run a command that requires local enviornment variables for one instance')
@click.option('-l', '--loadobj', default=False, type=click.BOOL, help='Load .env file as object instead of environment variable')
@click.option('-s', '--stringio', default=False, type=click.BOOL, help='Load .env file as StringIO object instead of environment variable')
@click.option('--clear', default=False, type=click.BOOL, help='Clear the environment variables set by pydotenvs or all variables during runtime.')
@click.option('-v', '--verbose', default=False, type=click.BOOL, help='Verbose')
@click.version_option(version=__version__)
def pyenv(envpath, newpath, transfer, preserve, command, loadobj, stringio, clear, verbose):
	if stringio:
		stringObj = load_env(env_path=envpath, stringIO=stringio, auto_close=True, verbose=verbose)  # without auto close, you're resposible for closing StringIO object
		click.echo(stringObj.getvalue())
		sys.exit()
	if loadobj:
		envDict = load_env_object(env_path=envpath, verbose=verbose)
		click.echo(envDict)
		sys.exit()
	if transfer:
		if newpath == None or newpath == '':
			click.echo('New env file path is required for transfer.')
			sys.exit()
		transfer_new_env(envpath, newpath, preserve)
		click.echo('Transfer complete.')
		sys.exit()
	if clear:
		user_input = input('Clear only the variables found in {}? (Y/n) '.format(envpath))
		if user_input.lower() != 'y' and user_input.lower() != 'n':
			click.echo('Invalid input given. Terminating.')
			sys.exit()
		clear_env(envpath, module_init_only=[True if user_input.lower() == 'y' else False][0])
		sys.exit()

	# if none are true do as normal
	load_env_cli(env_path=envpath, command=command, verbose=verbose)


if __name__ == '__main__':
	pyenv()

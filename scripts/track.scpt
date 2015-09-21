processes = Application("System Events").applicationProcesses;

function isRunning(app){
	try{
		processes[app]();
		return true;
	}catch(e){}
	return false;
}

if(isRunning("iTunes")){
	Application("iTunes").currentTrack.name();
}else if(isRunning("VOX")){
	Application("VOX").track();
}

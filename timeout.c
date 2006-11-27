/*++
 * NAME
 *	timeout 1
 * SUMMARY
 *	run command with bounded time
 * SYNOPSIS
 *	\fBtimeout\fR [-\fIsignal\fR] \fItime\fR \fIcommand\fR ...
 * DESCRIPTION
 *	\fBtimeout\fR executes a command and imposes an elapsed time limit.
 *	The command is run in a separate POSIX process group so that the
 *	right thing happens with commands that spawn child processes.
 *
 *	Arguments:
 * .IP \fI-signal\fR
 *	Specify an optional signal to send to the controlled process.
 *	By default, \fBtimeout\fR sends SIGKILL, which cannot be caught
 *	or ignored.
 * .IP \fItime\fR
 *	The elapsed time limit after which the command is terminated.
 * .IP \fIcommand\fR
 *	The command to be executed.
 * DIAGNOSTICS
 *	The command exit status is the exit status of the command
 *	(status 1 in case of a usage error).
 * AUTHOR(S)
 *	Wietse Venema
 *	This program is part of SATAN.
 *--
 */

/* System libraries. */

#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

extern int optind;

/* Application-specific. */

#define perrorexit(s) { perror(s); exit(1); }
#define WRITE(x) write(2, x, strlen(x))

static int kill_signal = SIGKILL;
static char *progname;
static char *commandname;

// fmt_ulong and fmt_long from libowfat {{{
unsigned int fmt_ulong(char *dest,unsigned long i) {
  register unsigned long len,tmp,len2;
  /* first count the number of bytes needed */
  for (len=1, tmp=i; tmp>9; ++len) tmp/=10;
  if (dest)
    for (tmp=i, dest+=len, len2=len+1; --len2; tmp/=10)
      *--dest = (tmp%10)+'0';
  return len;
}

unsigned int fmt_long(char *dest,long int i) {
  if (i<0) {
    if (dest) *dest++='-';
    return fmt_ulong(dest,-i)+1;
  } else
    return fmt_ulong(dest,i);
}
// }}}

static void usage()
{
    //fprintf(stderr, "usage: %s [-signal] time command...\n", progname);
    WRITE("usage: ");
    WRITE(progname);
    WRITE(" [-signal] time command...\n");
    exit(1);
}

static void terminate(int sig)
{
    signal(kill_signal, SIG_DFL);
    //fprintf(stderr, "Timeout: aborting command ``%s'' with signal %d\n",
    //    commandname, kill_signal);
    char kill_signal_string[22];
    fmt_long(kill_signal_string, kill_signal);
    WRITE("Timeout: aborting command ``");
    WRITE(commandname);
    WRITE("'' with signal ");
    WRITE(kill_signal_string);
    WRITE("\n");
    kill(0, kill_signal);
}

int main(int argc, char** argv)
{
    int     time_to_run = 0;
    pid_t   pid;
    pid_t   child_pid;
    int     status;

    progname = argv[0];

    /*
     * Parse JCL.
     */
    while (--argc && *++argv && **argv == '-')
	if ((kill_signal = atoi(*argv + 1)) <= 0)
	    usage();

    if (argc < 2 || (time_to_run = atoi(argv[0])) <= 0)
	usage();

    commandname = argv[1];

    /*
     * Run the command and its watchdog in a separate process group so that
     * both can be killed off with one signal.
     */
    setsid();
    switch (child_pid = fork()) {
    case -1:					/* error */
	perrorexit("timeout: fork");
    case  0:					/* run controlled command */
	execvp(argv[1], argv + 1);
	perrorexit(argv[1]);
    default:					/* become watchdog */
	(void) signal(SIGHUP, terminate);
	(void) signal(SIGINT, terminate);
	(void) signal(SIGQUIT, terminate);
	(void) signal(SIGTERM, terminate);
	(void) signal(SIGALRM, terminate);
	alarm(time_to_run);
	while ((pid = wait(&status)) != -1 && pid != child_pid)
	     /* void */ ;
	return (pid == child_pid ? status : -1);
    }
}

// vim: foldmethod=maker

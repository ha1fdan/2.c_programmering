// Monte Carlo estimation of Pi (parallel version)
// Usage: ./estimate-pi [runs] [threads]
// Default: runs = 10000000 (10 million), threads = number of online cores.
// Algorithm: Throw random points in [-1,1] x [-1,1]; Pi ≈ 4 * inside / total.
// Parallelization: Each thread performs an independent chunk of trials with its own RNG seed.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#include <unistd.h>

typedef struct {
	unsigned long long iterations;      // number of points to generate
	unsigned long long in_circle;       // result counter
	unsigned int seed;                  // per-thread seed for rand_r
} worker_arg_t;

static void *worker(void *ptr) {
	worker_arg_t *arg = (worker_arg_t *)ptr;
	unsigned long long local_in = 0ULL;
	unsigned int seed = arg->seed;
	for (unsigned long long i = 0ULL; i < arg->iterations; ++i) {
		// rand_r is thread-safe per seed
		double x = (double) rand_r(&seed) / (double) RAND_MAX * 2.0 - 1.0;
		double y = (double) rand_r(&seed) / (double) RAND_MAX * 2.0 - 1.0;
		if (x * x + y * y <= 1.0) {
			++local_in;
		}
	}
	arg->in_circle = local_in; // write back result
	return NULL;
}

int main(int argc, char *argv[]) {
	unsigned long long runs = 10000000ULL; // default iterations
	long threads = sysconf(_SC_NPROCESSORS_ONLN);
	if (threads < 1) threads = 1;

	// Parse CLI arguments
	if (argc > 1) {
		char *end = NULL;
		unsigned long long val = strtoull(argv[1], &end, 10);
		if (end != argv[1] && *end == '\0' && val > 0) {
			runs = val;
		} else {
			fprintf(stderr, "Invalid runs value '%s' – using default %llu\n", argv[1], runs);
		}
	}
	if (argc > 2) {
		char *end = NULL;
		long tval = strtol(argv[2], &end, 10);
		if (end != argv[2] && *end == '\0' && tval > 0) {
			threads = tval;
		} else {
			fprintf(stderr, "Invalid threads value '%s' – using default %ld\n", argv[2], threads);
		}
	}
	if ((unsigned long long)threads > runs) {
		// Cap threads so each has at least one iteration
		threads = (long)runs;
	}

	// Allocate thread structures
	pthread_t *tids = (pthread_t *)malloc(sizeof(pthread_t) * (size_t)threads);
	worker_arg_t *args = (worker_arg_t *)malloc(sizeof(worker_arg_t) * (size_t)threads);
	if (!tids || !args) {
		fprintf(stderr, "Allocation failed.\n");
		free(tids); free(args);
		return 1;
	}

	// Distribute iterations across threads
	unsigned long long base = runs / (unsigned long long)threads;
	unsigned long long rem  = runs % (unsigned long long)threads;

	struct timespec t0, t1;
	clock_gettime(CLOCK_MONOTONIC, &t0);

	for (long i = 0; i < threads; ++i) {
		unsigned long long iters = base + (i < (long)rem ? 1ULL : 0ULL);
		args[i].iterations = iters;
		args[i].in_circle = 0ULL;
		// Seed: combine time + thread index to reduce correlation
		args[i].seed = (unsigned int)(time(NULL) ^ (i * 0x9E3779B1u));
		int rc = pthread_create(&tids[i], NULL, worker, &args[i]);
		if (rc != 0) {
			fprintf(stderr, "Failed to create thread %ld (error %d)\n", i, rc);
			// Adjust threads count for joins later
			threads = i;
			break;
		}
	}

	unsigned long long total_in = 0ULL;
	for (long i = 0; i < threads; ++i) {
		pthread_join(tids[i], NULL);
		total_in += args[i].in_circle;
	}

	clock_gettime(CLOCK_MONOTONIC, &t1);
	double elapsed = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;

	unsigned long long out_circle = runs - total_in;
	double est_pi = 4.0 * (double) total_in / (double) runs;

	printf("Runs: %llu\nThreads: %ld\n", runs, threads);
	printf("Inside: %llu  Outside: %llu\n", total_in, out_circle);
	printf("Estimate of pi: %.20f\n", est_pi);
	printf("Elapsed time: %.6f s  (%.2f M points/s)\n", elapsed, (runs/1e6)/elapsed);

	free(tids);
	free(args);
	return 0;
}

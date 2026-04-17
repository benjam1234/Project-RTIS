#include <time.h>
#include <stdlib.h>
#include <stdio.h>

long long randommul(int max);
int compare_doubles(const void *a, const void *b);

int main()
{
	struct timespec start,end;
	srand(time( NULL ));//On initialise le créateur de nombre aléatoire

	int max=1000001;//le maximum de chaque facteur
	int n_iter=10000000;//On répète combien de fois la boucle
	double *time_total= malloc(n_iter*sizeof(double));//on créée le tableau contenant le temps de chaque itération(très gros tableau)

	for(int i=0;i<n_iter;i++)
		{
		clock_gettime(CLOCK_MONOTONIC,&start);//on initialise le compteur
		randommul(max);//On ititialise la fonction
		clock_gettime(CLOCK_MONOTONIC,&end);//on fait la différence
		time_total[i]=(end.tv_sec-start.tv_sec)*1e9+(end.tv_nsec-start.tv_nsec);//On le stock dans notre fonction
		}

        qsort(time_total, n_iter, sizeof(double), compare_doubles);
        //La fonction quick sort en C a besoin de savoir : le tableau ,sa taille,la taille de chaque entité(ici des double) et une fonction pour savoir
	//comment il compare les éléments (ici des double mais cela pourrait des int/float etc...
	// Affichage des résultats pour la Tâche 1
        printf("Min (0%%)   : %f nanosecondes\n", time_total[0]);
        printf("Q1 (25%%)   : %f nanosecondes\n", time_total[n_iter / 4]);
        printf("Q2 (50%%)   : %f nanosecondes\n", time_total[n_iter / 2]);
        printf("Q3 (75%%)   : %f nanosecondes\n", time_total[(n_iter * 3) / 4]);
        printf("Max (100%%) : %f nanosecondes\n", time_total[n_iter - 1]);
        free(time_total);//On libère la mémoire
	return 0;
}


long long randommul(int max)
{       //Notre fonction que l'on va tester
	long long mul1=rand()%max;//On crée un 1er nombre entre 1 et max
	long long mul2=rand()%max;//On créé un 2e nombre
	return mul1*mul2;//On retourne le produit des 2
}


int compare_doubles(const void *a, const void *b) {
    double arg1 = *(const double *)a;
    double arg2 = *(const double *)b;
    
    if (arg1 < arg2) return -1;  // Si a est plus petit, on le met avant
    if (arg1 > arg2) return 1;   // Si a est plus grand, on le met après
    return 0;                    // Si c'est égal, on ne touche à rien
}

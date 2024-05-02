#include <stdio.h>

int a = 5;
double pi = 3.14;

void print(int number)
{
	printf("Number equals: %i", number);
}

void main(void)
{
	int counter, number;
	scanf("%i", &number);
	print(number);
	for (int i = 0; i < 5; ++i)
	{
		counter = i * 2 + 1;
		printf("This is counter #%i\n", counter);
	}

	getchar();
	getchar();
}

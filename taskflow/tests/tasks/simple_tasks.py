from celery import task

@task
def add(one, two):
    return one + two

@task
def mult(one, two):
    return one * two

@task
def subt(one, two):
    return one - two


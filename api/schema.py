import graphene 
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Tasks
from django.contrib.auth.models import User

class TaskNode(DjangoObjectType):
    class Meta:
        model = Tasks
        fields = ("task", "ismarked")
        filter_fields = {"task":["exact", "icontains"], "ismarked": ["exact"]}
        interfaces = (relay.Node, )
        
class UserNode(DjangoObjectType):
    tasks = DjangoFilterConnectionField(TaskNode)

    class Meta:
        model = User
        fields = ("username", )
        filter_fields = ["username", ]
        interfaces = (relay.Node, )

    def resolve_tasks(root, info, **kwargs):
        return root.tasks.all()

class Query(graphene.ObjectType):
    views = graphene.Field(UserNode, email=graphene.String())
    # pages = DjangoFilterConnectionField(TaskType)

    def resolve_views(root, info, email=None, **kwargs):
        if email == None:
            return User.objects.all()
        
        user = User.objects.get(username=email) 
        return user
    
class addTask(relay.ClientIDMutation):
    class Input:
        task = graphene.String()
        email = graphene.String(required=True)
    success = graphene.Boolean()

    @classmethod  
    def mutate_and_get_payload(cls, root, info, task, email):
        user = User.objects.get(username=email)
        prev = len(user.tasks.filter(task=task))
        
        if prev > 0:
            return addTask(success=False)
        user.tasks.create(task=task)
        return addTask(success=True)
    
class addNew(relay.ClientIDMutation):
    class Input:
        task = graphene.String()
        email = graphene.String(required=True)
    success = graphene.Boolean()

    @classmethod  
    def mutate_and_get_payload(cls, root, info, email):
        try:
            User.objects.create(username=email)
            return addNew(success=True)
        except:
            return addNew(success=False)

class changeMarked(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        task = graphene.String()
    # success = graphene.Boolean()
    task = graphene.String()
    ismarked = graphene.Boolean()
    @classmethod  
    def mutate_and_get_payload(cls, root, info, email, task):
        user = User.objects.get(username=email)
        Task = user.tasks.get(task=task)
        Task.ismarked = not Task.ismarked
        Task.save()
        return changeMarked(task=Task.task, ismarked=Task.ismarked)

class Mutation(graphene.ObjectType):
    addNew = addNew.Field()
    addtask = addTask.Field()
    changeMarked = changeMarked.Field()
    deleteTask = graphene.Field(TaskNode, task=graphene.String(), email=graphene.String())
    clearAll = graphene.Int(command=graphene.String(), email=graphene.String())


        
        
    # def resolve_addTask(root, info, email, task):
    #     user = User.objects.get(username=email)
    #     prev = len(user.tasks.filter(task=task))
        
    #     if prev > 0:
    #         return 0
    #     user.tasks.create(task=task)
    #     return 1
        
    def resolve_changeMarked(root, info, email, task):
        user = User.objects.get(username=email)
        Task = user.tasks.get(task=task)
        Task.ismarked = not Task.ismarked
        Task.save()
    
    def resolve_deleteTask(root, info, email, task):
        user = User.objects.get(username=email)
        Task = user.tasks.get(task=task)
        
        if Task.ismarked:
            Task.delete()
            return None
        return Task
    
    def resolve_clearAll(root, info, email, command):
        user = User.objects.get(username=email)
        tasks = user.tasks.all()

        if command == "marked":
            tasks = user.tasks.filter(ismarked=True)
        tasks.delete()



schema = graphene.Schema(query=Query, mutation=Mutation)
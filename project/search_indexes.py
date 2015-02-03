import datetime
from haystack import indexes
from project.models import BlogPost

class BlogPostIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	author = indexes.CharField(model_attr='author')
	added = indexes.CharField(model_attr='added')

	def get_model(self):
		return BLogPost

	def index_queryset(self, using=None):
		""" Used when the entire index for model is updated """
		return self.get_model().objects.filter(added__lte=datetime.datetime.now())
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Account
from engines.gdb.utils import get_gdb


class DataMixin(object):

    def get_gdb(self):
        try:
            if self.instance:
                return self.instance.get_gdb(graph=self.graph)
            else:
                return get_gdb(graph=self.graph)
        except ObjectDoesNotExist:
            if self.instance:
                return self.instance.get_gdb()
            else:
                return get_gdb()

    def can_add_nodes(self):
        user = self.graph.owner
        if user.is_superuser or user.is_staff:
            return True
        else:
            try:
                profile = user.get_profile()
                # HACK: Avoid the QuerySet cache
                account = Account.objects.get(pk=profile.account.id)
                return (self.total_nodes < account.nodes)
            except:
                return False

    def can_add_relationships(self):
        user = self.graph.owner
        if user.is_superuser or user.is_staff:
            return True
        else:
            try:
                profile = user.get_profile()
                # HACK: Avoid the QuerySet cache
                account = Account.objects.get(pk=profile.account.id)
                return (self.total_relationships < account.relationships)
            except:
                return False

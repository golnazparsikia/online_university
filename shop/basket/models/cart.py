# from django.db import models
# from design.state import PendingState, ConfirmedState

# class Cart(models.Model):
#     user = models.ForeignKey(

#         on_delete=models.CASCADE
#         )
#     state = models.CharField(
#         max_length=20
#         ) 

#     def change_state(self, new_state):
#         self.state = new_state
#         self.save()

#     def process_order(self):
#         state_classes = {
#             'pending': PendingState(),
#             'confirmed': ConfirmedState(),
#         }
#         current_state = state_classes.get(self.state)
#         if current_state:
#             current_state.process_order(self)
#         else:
#             print("Invalid state.")
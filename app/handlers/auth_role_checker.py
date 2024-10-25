from fastapi.responses import RedirectResponse
from typing import List
 
def auth_and_roles_required(current_user, 
                            required_roles: List[str]):
   if current_user is None:
       return False
   if current_user.role.name in required_roles:
       return True
   return False

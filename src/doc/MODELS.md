Model planning Arcitecture

Membership
    -slug
    -type (free,pro,enterprise)
    -price
    -stripe plan id 

userMembership
    -user                      (foreginkey to default user)
    -stripe customer id
    -membership type           (foreginkey to Membership)
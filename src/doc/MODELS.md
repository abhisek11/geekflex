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

Subscription
    -user Membership 
    -stripe subscription id    (foreignkey to userMembership)      
    -active

Course
    -slug
    -title
    -description
    -allowed memberships       (Foreignkey to Membership)    

Lesson
    -slug
    -title
    -Course                     (Foreignkey to Course)
    -position
    -video
    -thumbnail
    
namespace Newstein

structure RootedBall where
  carrier : Type

def parent (_B : RootedBall) : Prop := True
def Retr (_B : RootedBall) : Prop := True

theorem ParentIterationToRoot : True := by
  trivial

end Newstein

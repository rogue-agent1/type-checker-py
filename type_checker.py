#!/usr/bin/env python3
"""Type checker for a simple typed expression language."""
class Type:pass
class IntType(Type):
    def __repr__(self):return"int"
    def __eq__(self,o):return isinstance(o,IntType)
    def __hash__(self):return hash("int")
class BoolType(Type):
    def __repr__(self):return"bool"
    def __eq__(self,o):return isinstance(o,BoolType)
    def __hash__(self):return hash("bool")
class FunType(Type):
    def __init__(self,arg,ret):self.arg=arg;self.ret=ret
    def __repr__(self):return f"({self.arg} -> {self.ret})"
    def __eq__(self,o):return isinstance(o,FunType) and self.arg==o.arg and self.ret==o.ret
class Expr:pass
class Lit(Expr):
    def __init__(self,val,typ):self.val=val;self.typ=typ
class Var(Expr):
    def __init__(self,name):self.name=name
class App(Expr):
    def __init__(self,fn,arg):self.fn=fn;self.arg=arg
class Lam(Expr):
    def __init__(self,param,param_type,body):self.param=param;self.param_type=param_type;self.body=body
class If(Expr):
    def __init__(self,cond,then,else_):self.cond=cond;self.then=then;self.else_=else_
class BinOp(Expr):
    def __init__(self,op,l,r):self.op=op;self.l=l;self.r=r
def typecheck(expr,env=None):
    if env is None:env={}
    if isinstance(expr,Lit):return expr.typ
    if isinstance(expr,Var):
        if expr.name not in env:raise TypeError(f"Unbound: {expr.name}")
        return env[expr.name]
    if isinstance(expr,Lam):
        new_env=dict(env);new_env[expr.param]=expr.param_type
        ret=typecheck(expr.body,new_env)
        return FunType(expr.param_type,ret)
    if isinstance(expr,App):
        ft=typecheck(expr.fn,env);at=typecheck(expr.arg,env)
        if not isinstance(ft,FunType):raise TypeError(f"Not a function: {ft}")
        if ft.arg!=at:raise TypeError(f"Arg type mismatch: expected {ft.arg}, got {at}")
        return ft.ret
    if isinstance(expr,If):
        ct=typecheck(expr.cond,env)
        if ct!=BoolType():raise TypeError(f"Condition must be bool, got {ct}")
        tt=typecheck(expr.then,env);et=typecheck(expr.else_,env)
        if tt!=et:raise TypeError(f"Branch type mismatch: {tt} vs {et}")
        return tt
    if isinstance(expr,BinOp):
        lt=typecheck(expr.l,env);rt=typecheck(expr.r,env)
        if expr.op in ["+","-","*"]:
            if lt!=IntType() or rt!=IntType():raise TypeError("Int expected")
            return IntType()
        if expr.op in ["<",">"]:
            if lt!=IntType() or rt!=IntType():raise TypeError("Int expected")
            return BoolType()
        if expr.op in ["&&","||"]:
            if lt!=BoolType() or rt!=BoolType():raise TypeError("Bool expected")
            return BoolType()
    raise TypeError(f"Unknown expr: {expr}")
def main():
    e=Lam("x",IntType(),BinOp("+",Var("x"),Lit(1,IntType())))
    print(f"Type: {typecheck(e)}")
    e2=App(e,Lit(5,IntType()));print(f"App type: {typecheck(e2)}")
if __name__=="__main__":main()

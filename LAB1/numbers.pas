unit Numbers;

{$mode objfpc}{$H+}

interface

procedure GenerateRandom(var Arr: array of Integer);

implementation

procedure GenerateRandom(var Arr: array of Integer);
var
  I: Integer;
begin
  Randomize;
  for I := 0 to High(Arr) do
    Arr[I] := Random(101);
end;

end.

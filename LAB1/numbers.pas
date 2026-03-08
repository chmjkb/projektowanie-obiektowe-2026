unit Numbers;

{$mode objfpc}{$H+}

interface

procedure GenerateRandom(var Arr: array of Integer; MinVal: Integer; MaxVal: Integer);
procedure SortNumbers(var Arr: array of Integer);

implementation

procedure GenerateRandom(var Arr: array of Integer; MinVal: Integer; MaxVal: Integer);
var
  I: Integer;
begin
  Randomize;
  for I := 0 to High(Arr) do
    Arr[I] := MinVal + Random(MaxVal - MinVal + 1);
end;

procedure SortNumbers(var Arr: array of Integer);
var
  I, J, Temp: Integer;
begin
  for I := 0 to High(Arr) - 1 do
    for J := 0 to High(Arr) - I - 1 do
      if Arr[J] > Arr[J + 1] then
      begin
        Temp := Arr[J];
        Arr[J] := Arr[J + 1];
        Arr[J + 1] := Temp;
      end;
end;

end.

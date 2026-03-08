program Tests;

{$mode objfpc}{$H+}

uses
  fpcunit, testregistry, consoletestrunner, Numbers;

type
  TNumbersTest = class(TTestCase)
  published
    procedure TestGenerateRandomInRange;
    procedure TestGenerateRandomCustomRange;
    procedure TestSortAscending;
    procedure TestSortPreservesElements;
    procedure TestSortSingleElement;
  end;

{ Verifies all 50 generated numbers fall within the default 0-100 range }
procedure TNumbersTest.TestGenerateRandomInRange;
var
  Arr: array[0..49] of Integer;
  I: Integer;
begin
  GenerateRandom(Arr, 0, 100);
  for I := 0 to 49 do
  begin
    AssertTrue('Number should be >= 0', Arr[I] >= 0);
    AssertTrue('Number should be <= 100', Arr[I] <= 100);
  end;
end;

{ Verifies all generated numbers fall within a custom range }
procedure TNumbersTest.TestGenerateRandomCustomRange;
var
  Arr: array[0..9] of Integer;
  I: Integer;
begin
  GenerateRandom(Arr, 10, 50);
  for I := 0 to 9 do
  begin
    AssertTrue('Number should be >= 10', Arr[I] >= 10);
    AssertTrue('Number should be <= 50', Arr[I] <= 50);
  end;
end;

{ Verifies that after sorting, array is in ascending order }
procedure TNumbersTest.TestSortAscending;
var
  Arr: array[0..4] of Integer;
  I: Integer;
begin
  Arr[0] := 5; Arr[1] := 3; Arr[2] := 8; Arr[3] := 1; Arr[4] := 9;
  SortNumbers(Arr);
  for I := 0 to 3 do
    AssertTrue('Array should be sorted in ascending order', Arr[I] <= Arr[I + 1]);
end;

{ Verifies sorting does not lose or duplicate any elements (sum must be preserved) }
procedure TNumbersTest.TestSortPreservesElements;
var
  Arr: array[0..4] of Integer;
  SumBefore, SumAfter, I: Integer;
begin
  Arr[0] := 5; Arr[1] := 3; Arr[2] := 8; Arr[3] := 1; Arr[4] := 4;
  SumBefore := 0;
  for I := 0 to 4 do
    SumBefore := SumBefore + Arr[I];
  SortNumbers(Arr);
  SumAfter := 0;
  for I := 0 to 4 do
    SumAfter := SumAfter + Arr[I];
  AssertEquals('Sum should be preserved after sorting', SumBefore, SumAfter);
end;

{ Verifies sorting works correctly on a single-element array }
procedure TNumbersTest.TestSortSingleElement;
var
  Arr: array[0..0] of Integer;
begin
  Arr[0] := 42;
  SortNumbers(Arr);
  AssertEquals('Single element array should remain unchanged', 42, Arr[0]);
end;

var
  Application: TTestRunner;
begin
  Application := TTestRunner.Create(nil);
  Application.Initialize;
  Application.Title := 'Numbers Unit Tests';
  Application.Run;
  Application.Free;
end.
